"""PIL Generator (repo-scanner) - minimal PILScanner skeleton and utilities.

This module provides a `PILScanner` class with the minimal state and utility
functions required by the PIL specification. The implementation focuses on
deterministic, testable behavior and safe handling of missing files.
"""

from __future__ import annotations

import ast
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import xml.etree.ElementTree as ET
import re

MISSING_FILE_HASH = "MISSING_FILE_HASH"

logger = logging.getLogger("pil.scanner")
logger.addHandler(logging.NullHandler())


class PILScanner:
    """Scanner class responsible for reading PIL contracts and running checks.

    This skeleton implements core utilities used by later scoring and analysis
    routines. Methods intentionally keep behavior deterministic and safe when
    files are missing.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo_contract_path = self.repo_path / "repo_contract.yml"
        self.project_map_path = self.repo_path / "project_map.yml"
        self.scoring_kpis_path = self.repo_path / "scoring_kpis.yml"
        self.task_contract_path = self.repo_path / "task_contract.yml"

        # in-memory caches
        self._hash_cache: Dict[str, str] = {}
        self._loaded_repo_contract: Optional[Dict[str, Any]] = None

    # ------------------------ Utility functions ------------------------
    def calculate_artifact_hash(self, file_path: str) -> str:
        """Return SHA-256 hex digest for `file_path`.

        If the file does not exist, return the deterministic sentinel
        `MISSING_FILE_HASH` rather than raising.
        """
        p = Path(file_path)
        try:
            with p.open("rb") as fh:
                h = hashlib.sha256()
                while True:
                    chunk = fh.read(8192)
                    if not chunk:
                        break
                    h.update(chunk)
                digest = h.hexdigest()
                # cache for single-run efficiency
                self._hash_cache[str(p)] = digest
                return digest
        except FileNotFoundError:
            return MISSING_FILE_HASH

    def ast_check(self, file_path: str, required_signature: Any) -> Tuple[bool, str]:
        """Perform a light AST-based compliance check.

        `required_signature` can be one of:
         - a string: function name that must be present
         - a dict: {"function": name, "params": [p1, p2], "decorator": "name"}

        Returns (is_compliant, diagnostic_message).
        """
        p = Path(file_path)
        if not p.exists():
            return False, f"File not found: {file_path}"

        try:
            src = p.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except Exception as e:
            return False, f"AST parse error: {e}"

        # Normalize required_signature
        if isinstance(required_signature, str):
            func_name = required_signature
            required_params = None
            decorator = None
        elif isinstance(required_signature, dict):
            func_name = required_signature.get("function")
            required_params = required_signature.get("params")
            decorator = required_signature.get("decorator")
        else:
            return False, "Unsupported required_signature format"

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if func_name and node.name != func_name:
                    continue

                # check params if requested
                if required_params is not None:
                    arg_names = [a.arg for a in node.args.args]
                    # drop 'self' when present for methods
                    if arg_names and arg_names[0] == "self":
                        arg_names = arg_names[1:]
                    if arg_names != required_params:
                        return (
                            False,
                            f"Function '{node.name}' parameters mismatch: expected {required_params}, found {arg_names}",
                        )

                # check decorator if requested
                if decorator:
                    dec_names = []
                    for d in node.decorator_list:
                        if isinstance(d, ast.Name):
                            dec_names.append(d.id)
                        elif isinstance(d, ast.Attribute):
                            dec_names.append(d.attr)
                        else:
                            dec_names.append(ast.dump(d))
                    if decorator not in dec_names:
                        return (
                            False,
                            f"Decorator '{decorator}' not found on function '{node.name}' (found: {dec_names})",
                        )

                # all requested checks passed for this function
                return True, f"Function '{node.name}' compliant"

        return False, f"Required function '{func_name}' not found in {file_path}"

    # ------------------------ Implementation signal scanners ------------------
    def _gather_python_files(self) -> List[Path]:
        """Return a sorted list of .py files under the repository (deterministic)."""
        files = []
        for p in sorted(self.repo_path.rglob("*.py")):
            # skip common virtualenv or hidden dirs
            if any(part.startswith(".") or part in (".venv", "venv", "__pycache__") for part in p.parts):
                continue
            files.append(p)
        return files

    def discover_impl_files(self, declared_impl_files: Optional[List[str]] = None) -> List[str]:
        """Discover implementation .py files under `src/`.

        Rules:
        - Scan `src/` recursively for `.py` modules
        - Exclude any path segment named `tests` or files starting with `test_`
        - Exclude `__pycache__` directories
        - Return absolute, resolved string paths
        - Deduplicate with `declared_impl_files` (exclude declared paths from results)
        """
        out: List[str] = []
        src_root = self.repo_path / "src"
        declared_set = set()
        if declared_impl_files:
            for f in declared_impl_files:
                try:
                    p = Path(f)
                    if not p.is_absolute():
                        p = (self.repo_path / p).resolve()
                    else:
                        p = p.resolve()
                    declared_set.add(str(p))
                except Exception:
                    continue

        if not src_root.exists():
            return []

        for p in sorted(src_root.rglob("*.py")):
            # skip __pycache__ and hidden/venv dirs
            if any(part in ("__pycache__", "venv", ".venv") for part in p.parts):
                continue
            # skip tests folders or files beginning with test_
            if any(part.lower() == "tests" for part in p.parts):
                continue
            if p.name.startswith("test_") or p.name.startswith("tests_"):
                continue
            try:
                rp = p.resolve()
                rs = str(rp)
                if rs in declared_set:
                    # deduplicate: do not return declared files
                    continue
                out.append(rs)
            except Exception:
                continue

        return out

    def scan_structure(self, pm: Dict[str, Any], impl_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Collect simple structural signals and compute percent structure complete.

        The function checks for presence of expected folders and counts modules
        and folders. The expected items list is conservative and deterministic.
        """
        # Prefer scanning the provided implementation files to focus the
        # complexity/profile on the task-level code. If none provided, attempt
        # to derive implementation files from the supplied `pm` (project_map);
        # otherwise fall back to scanning all python files in the repository.
        py_files = []
        if impl_files:
            for f in impl_files:
                try:
                    p = Path(f)
                    if not p.is_absolute():
                        p = (self.repo_path / p).resolve()
                    else:
                        p = p.resolve()
                    if p.exists():
                        py_files.append(p)
                except Exception:
                    continue
        else:
            # derive any declared implementation_files from project_map
            declared = []
            try:
                for entry in (pm or {}).values():
                    if isinstance(entry, dict):
                        for f in entry.get("implementation_files", []) or []:
                            if isinstance(f, str):
                                declared.append(str((self.repo_path / f).resolve()))
            except Exception:
                declared = []

            for f in declared:
                try:
                    p = Path(f)
                    if p.exists():
                        py_files.append(p)
                except Exception:
                    continue

            # if no declared files found or declared list incomplete, attempt
            # to discover implementation files under src/ as a fallback
            if not py_files:
                # new helper will find python modules under src/ excluding tests
                discovered = self.discover_impl_files(declared)
                for f in discovered:
                    try:
                        p = Path(f)
                        if p.exists():
                            py_files.append(p)
                    except Exception:
                        continue
            if not py_files:
                py_files = self._gather_python_files()
        module_count = len(py_files)
        folder_set = set()
        for f in py_files:
            try:
                rel = os.path.relpath(str(f.parent), start=str(self.repo_path))
            except Exception:
                rel = str(f.parent)
            folder_set.add(rel)
        folder_count = len(folder_set)

        present = {}
        present["src/"] = (self.repo_path / "src").exists()
        present["pipelines/"] = any("pipeline" in str(p).lower() or "stages" in str(p).lower() for p in py_files)
        present["adapters/"] = any("adapter" in p.name.lower() or "/adapters/" in str(p).lower() for p in py_files)
        present["validators/"] = any("validator" in p.name.lower() or "validate" in p.name.lower() for p in py_files)
        present["tests/"] = (self.repo_path / "test-reports").exists() or any("test_" in p.name or p.name.startswith("test") for p in py_files)
        present["schemas/"] = any(p.suffix in (".json", ".yaml", ".yml") and "schema" in p.name.lower() for p in sorted(self.repo_path.rglob("*.*")))
        # CLI entrypoint heuristics
        present["cli_entry"] = any(p.name in ("cli.py", "main.py") or (p.name == "__main__.py") for p in py_files)

        # expected count inferred conservatively from project_map if present
        expected_items = ["src/", "pipelines/", "adapters/", "validators/", "tests/", "schemas/", "cli_entry"]
        present_count = sum(1 for k in expected_items if present.get(k))
        # Compute percent_structure_complete using declared and inferred signals.
        # Determine declared files from project_map and any discovered modules.
        declared_files = []
        try:
            for entry in (pm or {}).values():
                if isinstance(entry, dict):
                    for f in entry.get("implementation_files", []) or []:
                        if isinstance(f, str):
                            declared_files.append(str((self.repo_path / f).resolve()))
        except Exception:
            declared_files = []

        # Attempt to discover impl files under src/ to complement declared entries
        discovered = self.discover_impl_files(declared_files)

        declared_found = 0
        for f in declared_files:
            try:
                if Path(f).exists():
                    declared_found += 1
            except Exception:
                continue

        total_declared = len(declared_files)
        inferred_detected = len(discovered)
        inferred_expected = len(discovered) if discovered else 1

        # Combine declared completeness and inferred completeness by summing
        # as specified: declared_ratio + inferred_ratio, cap at 1.0
        declared_ratio = (declared_found / total_declared) if total_declared > 0 else 0.0
        inferred_ratio = (inferred_detected / inferred_expected) if inferred_expected > 0 else 0.0
        combined = declared_ratio + inferred_ratio
        if combined > 1.0:
            combined = 1.0
        percent_structure = int(round(combined * 100.0))

        # If declared files are missing but code exists (inferred detected or any py_files),
        # do not allow structure percent to drop below 50% (neutral). This enforces
        # that missing metadata does not fully penalize structure completeness.
        code_exists = bool(py_files)
        if total_declared == 0 and code_exists and percent_structure < 50:
            percent_structure = 50

        return {
            "module_count": module_count,
            "folder_count": folder_count,
            "present": present,
            "percent_structure_complete": percent_structure,
        }

    def scan_implementation_signals(self, impl_files: List[str], task_id: str) -> Dict[str, Any]:
        """Scan repository for implementation signals relevant to a task.

        Returns counts for modules, functions, classes, pipeline stages, validators, adapters.
        """
        # Prefer scanning the provided implementation files to focus the
        # complexity/profile on the task-level code. If none provided, fall
        # back to scanning all python files in the repository.
        if impl_files:
            py_files = []
            for f in impl_files:
                try:
                    p = Path(f)
                    if p.exists():
                        py_files.append(p)
                except Exception:
                    continue
        else:
            py_files = self._gather_python_files()
        modules_found = 0
        functions_found = 0
        classes_found = 0
        pipeline_stages_detected = 0
        validators_detected = 0
        adapters_detected = 0

        # helper lower task id
        tid_lower = (task_id or "").lower()

        for p in py_files:
            try:
                src = p.read_text(encoding="utf-8")
                tree = ast.parse(src)
            except Exception:
                continue
            # module-level name checks (validators module)
            try:
                lname = p.name.lower()
                if lname == "validators.py" or lname.endswith("_validators.py"):
                    validators_detected += 1
            except Exception:
                pass

            # detect imports referencing pipeline modules at the file level
            file_imports_pipeline = False
            for n in ast.walk(tree):
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    if isinstance(n, ast.Import):
                        for a in n.names:
                            an = (a.name or "").lower()
                            if any(k in an for k in ("pipeline", "stage", "stages")):
                                file_imports_pipeline = True
                                break
                    else:
                        mod = (n.module or "").lower()
                        if any(k in mod for k in ("pipeline", "stage", "stages")):
                            file_imports_pipeline = True
                            break

            file_has_impl = False
            # detect imports that reference pipeline modules (e.g. import pipelines.x)
            file_imports_pipeline = False
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    # handle Import
                    if isinstance(node, ast.Import):
                        for a in node.names:
                            nm = (a.name or "").lower()
                            if "pipeline" in nm or "stage" in nm or "stages" in nm:
                                file_imports_pipeline = True
                                break
                    else:
                        # ImportFrom
                        mod = (node.module or "").lower()
                        if "pipeline" in mod or "stage" in mod or "stages" in mod:
                            file_imports_pipeline = True
                            break

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions_found += 1
                    file_has_impl = True
                    name = node.name.lower()
                    # pipeline stage heuristics
                    dec_has_stage = any((isinstance(d, ast.Name) and "stage" in d.id.lower()) or (isinstance(d, ast.Attribute) and "stage" in getattr(d, "attr", "").lower()) for d in node.decorator_list)
                    if "stage" in name or "pipeline" in name or dec_has_stage:
                        pipeline_stages_detected += 1
                    if tid_lower and tid_lower in name:
                        modules_found += 1
                    # validator heuristics: functions named *validate* OR functions
                    # with a single non-self argument that return boolean-like values
                    try:
                        if "validate" in name:
                            validators_detected += 1
                        else:
                            # count args (allow methods with 'self')
                            args_len = len(node.args.args)
                            arg_ok = args_len == 1 or (args_len == 2 and node.args.args and node.args.args[0].arg == 'self')
                            if arg_ok:
                                # inspect returns for boolean-like expressions
                                has_bool_return = False
                                for sub in ast.walk(node):
                                    if isinstance(sub, ast.Return) and sub.value is not None:
                                        rv = sub.value
                                        if isinstance(rv, ast.Constant) and isinstance(rv.value, bool):
                                            has_bool_return = True
                                            break
                                        if isinstance(rv, (ast.Compare, ast.BoolOp, ast.UnaryOp)):
                                            has_bool_return = True
                                            break
                                if has_bool_return:
                                    validators_detected += 1
                    except Exception:
                        pass
                if isinstance(node, ast.ClassDef):
                    classes_found += 1
                    file_has_impl = True
                    name = node.name.lower()
                    if "validator" in name or "validate" in name:
                        validators_detected += 1
                    if "adapter" in name:
                        adapters_detected += 1

                # detect top-level calls to validator factories
                if isinstance(node, ast.Call):
                    fn = node.func
                    fname = None
                    if isinstance(fn, ast.Name):
                        fname = fn.id.lower()
                    elif isinstance(fn, ast.Attribute):
                        fname = getattr(fn, "attr", "").lower()
                    if fname and ("validate" in fname or "schema" in fname):
                        validators_detected += 1

            if file_has_impl and (tid_lower and tid_lower in p.name.lower()):
                modules_found += 1

            # if file imports indicate pipeline linking, attribute one detection
            if file_imports_pipeline:
                pipeline_stages_detected += 1

        # normalize modules_found: cap at 1 per task signal
        modules_found = min(modules_found, len(py_files))

        return {
            "modules_found": modules_found,
            "functions_found": functions_found,
            "classes_found": classes_found,
            "pipeline_stages_detected": pipeline_stages_detected,
            "validators_detected": validators_detected,
            "adapters_detected": adapters_detected,
        }

    def check_state_transition_implemented(self, impl_files: List[str]) -> Tuple[bool, List[str]]:
        """Detect simple state-transition implementations in given files.

        Heuristic (best-effort): returns True if any implementation file
        contains either:
          - a function decorated with `@state_transition` (decorator name), or
          - a function named `apply_state_transition` or `transition_state`.

        Returns (found: bool, details: [diagnostics]). This is deterministic
        and conservative; it does not attempt to interpret runtime semantics.
        """
        diagnostics: List[str] = []
        found = False

        # helper sets of known call/function names that often indicate transitions
        transition_call_names = {"set_state", "change_state", "next_state", "transition_state", "apply_state", "apply_changes"}

        for f in impl_files:
            try:
                p = Path(f)
                if not p.exists():
                    diagnostics.append(f"missing:{f}")
                    continue
                src = p.read_text(encoding="utf-8")
                tree = ast.parse(src)
            except Exception as e:
                diagnostics.append(f"parse_error:{f}:{e}")
                continue

            # scan AST for multiple heuristic signals
            for node in ast.walk(tree):
                # 1) function name or decorated function
                if isinstance(node, ast.FunctionDef):
                    name_lower = node.name.lower()
                    if "transition" in name_lower or name_lower.startswith("apply_") and "transition" in name_lower:
                        found = True
                        diagnostics.append(f"found_function:{node.name}@{f}")
                        break

                    # decorator check
                    dec_names = set()
                    for d in node.decorator_list:
                        # handle simple names, attributes, and calls (e.g. @decorator(), @pkg.decorator)
                        if isinstance(d, ast.Name):
                            dec_names.add(d.id)
                        elif isinstance(d, ast.Attribute):
                            dec_names.add(getattr(d, "attr", ""))
                        elif isinstance(d, ast.Call):
                            # decorator with call: inspect the underlying function
                            func = d.func
                            if isinstance(func, ast.Name):
                                dec_names.add(func.id)
                            elif isinstance(func, ast.Attribute):
                                dec_names.add(getattr(func, "attr", ""))
                        else:
                            try:
                                dec_names.add(ast.unparse(d))
                            except Exception:
                                pass

                    known = {"state_transition", "transition", "state_change", "transition_decorator"}
                    if dec_names & known:
                        found = True
                        diagnostics.append(f"decorator_state_transition:{node.name}@{f}:{sorted(list(dec_names & known))}")
                        break

                    # detect functions that take a 'state' param and return something -> likely transition
                    arg_names = [a.arg for a in node.args.args]
                    if arg_names and ("state" in arg_names or "old_state" in arg_names or "current_state" in arg_names):
                        # ensure function has a return statement
                        has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                        if has_return:
                            found = True
                            diagnostics.append(f"func_with_state_param_and_return:{node.name}@{f}:{arg_names}")
                            break

                # 2) assignment to `.state` attribute (obj.state = ... or self.state = ...)
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Attribute) and getattr(target, "attr", "") in ("state", "status"):
                            found = True
                            diagnostics.append(f"assign_attr_state:{f}:{ast.unparse(target) if hasattr(ast, 'unparse') else 'attr'}")
                            break
                    if found:
                        break

                # 3) calls to well-known transition helpers
                if isinstance(node, ast.Call):
                    # extract simple call name
                    func_name = None
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        func_name = getattr(node.func, "attr", None)

                    if func_name and func_name in transition_call_names:
                        found = True
                        diagnostics.append(f"call_transition_helper:{func_name}@{f}")
                        break

            if found:
                # stop early as one signal suffices
                break

        return found, diagnostics

    # ------------------------ Pre-scan gates ------------------------
    def run_sanity_gate(self) -> Dict[str, Any]:
        """Evaluate `repo_contract.yml` sanity checks and return health object.

        The returned structure is deterministic and never raises; missing contract
        files are treated as failing checks.
        """
        result: Dict[str, Any] = {"healthy": False, "details": {}}

        # Load repo_contract if possible (YAML optional; keep simple JSON-like fallback)
        try:
            import yaml

            if self.repo_contract_path.exists():
                self._loaded_repo_contract = yaml.safe_load(self.repo_contract_path.read_text(encoding="utf-8"))
        except Exception:
            # keep _loaded_repo_contract as None if yaml not available or file missing
            self._loaded_repo_contract = None

        checks = []
        if self._loaded_repo_contract and isinstance(self._loaded_repo_contract, dict):
            checks = self._loaded_repo_contract.get("sanity_checks", [])

        # By default only a few items are strictly required. Other items are
        # warnings and should not block scoring. This implements the new
        # requirement: only fail sanity if project_map or scoring_kpis missing,
        # or src/ missing AND code-based KPIs cannot run.
        details = {}
        blocked = False

        # required critical checks
        project_map_ok = self.project_map_path.exists()
        scoring_ok = self.scoring_kpis_path.exists()
        src_ok = (self.repo_path / "src").exists()

        details["project_map.yml"] = bool(project_map_ok)
        details["scoring_kpis.yml"] = bool(scoring_ok)
        details["src/"] = bool(src_ok)

        # If project_map or scoring_kpis are missing -> block
        if not project_map_ok or not scoring_ok:
            blocked = True

        # If src missing, determine whether code-based KPIs can run by scanning
        # for any python files outside src. If none, block; else warn but continue.
        if not src_ok:
            py_files = self._gather_python_files()
            if not py_files:
                # no code found -> cannot compute implementation KPIs
                details["code_present_elsewhere"] = False
                blocked = True
            else:
                details["code_present_elsewhere"] = True
                # do not block; emit warning only

        # populate any additional checks as non-blocking warnings
        if self._loaded_repo_contract and isinstance(self._loaded_repo_contract, dict):
            for c in self._loaded_repo_contract.get("sanity_checks", []):
                if c in ("project_map.yml", "scoring_kpis.yml", "src/"):
                    continue
                # interpret directory markers ending with '/'
                if isinstance(c, str) and c.endswith("/"):
                    ok = (self.repo_path / c.rstrip("/")).exists()
                else:
                    if isinstance(c, str) and c == "checklist.yml":
                        ok = (self.repo_path / c).exists() or (self.repo_path / "docs" / c).exists()
                    else:
                        ok = (self.repo_path / c).exists()
                details[str(c)] = bool(ok)

        result["healthy"] = not blocked
        result["details"] = details
        return result

    # ------------------------ Drift & Dependencies (skeletons) -----------------
    def version_and_drift_detection(self, last_hashes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Compare current artifact hashes against `last_hashes` to identify deltas.

        Returns a deterministic structure:
          {
            "changed": [filepaths],
            "unchanged": [filepaths],
            "missing": [filepaths],
            "details": { filepath: {"previous": <hex|None>, "current": <hex|MISSING_FILE_HASH>} }
          }

        Implementation notes:
        - Reads `project_map.yml` and inspects `implementation_files` lists.
        - All paths are resolved relative to `self.repo_path`.
        - Missing files are reported under `missing` and have `current` == `MISSING_FILE_HASH`.
        - Any exception is non-fatal and will be logged; the function attempts best-effort behavior.
        """

        deltas: Dict[str, Any] = {"changed": [], "unchanged": [], "missing": [], "details": {}}
        try:
            import yaml

            pm: Dict[str, Any] = {}
            if self.project_map_path.exists():
                pm = yaml.safe_load(self.project_map_path.read_text(encoding="utf-8")) or {}

            files = set()
            for entry in pm.values():
                if isinstance(entry, dict):
                    for f in entry.get("implementation_files", []) or []:
                        # support both string paths and nested lists defensively
                        if isinstance(f, str):
                            files.add(str((self.repo_path / f).resolve()))
            # deterministically iterate
            for f in sorted(files):
                cur = self.calculate_artifact_hash(f)
                prev = (last_hashes or {}).get(f)
                deltas["details"][f] = {"previous": prev, "current": cur}
                if cur == MISSING_FILE_HASH:
                    deltas["missing"].append(f)
                elif prev is None:
                    # new or untracked file -> treated as changed
                    deltas["changed"].append(f)
                elif prev != cur:
                    deltas["changed"].append(f)
                else:
                    deltas["unchanged"].append(f)

        except Exception as exc:  # pragma: no cover - best-effort path
            logger.exception("version_and_drift_detection failed: %s", exc)

        return deltas

    def parse_junit_reports(self) -> Dict[str, bool]:
        """Parse JUnit-style XML reports under `test-reports/`.

        Returns a mapping of keys -> boolean where keys take the form
        `file::testname` or `classname::testname` or `testname` and the value
        indicates whether the test passed (True) or failed/skipped (False).
        This is best-effort and non-fatal if files are missing or malformed.
        """
        out: Dict[str, bool] = {}
        reports_dir = self.repo_path / "test-reports"
        if not reports_dir.exists():
            return out

        for p in sorted(reports_dir.glob("*.xml")):
            try:
                tree = ET.parse(str(p))
                root = tree.getroot()
                for tc in root.iter("testcase"):
                    name = tc.attrib.get("name")
                    classname = tc.attrib.get("classname") or ""
                    file_attr = tc.attrib.get("file") or ""

                    if file_attr:
                        key = f"{file_attr}::{name}"
                    elif classname:
                        key = f"{classname}::{name}"
                    else:
                        key = name or ""

                    passed = True
                    # if testcase has child elements like failure/error/skipped -> not passed
                    for child in list(tc):
                        tag = child.tag.lower()
                        if tag in ("failure", "error", "skipped"):
                            passed = False
                            break

                    if key:
                        out[key] = passed
            except Exception:
                # non-fatal: skip malformed report
                continue

        return out

    def check_dependencies(self, task_id: str, repos_index: Dict[str, Any]) -> Dict[str, Any]:
        """Verify prerequisites for `task_id` using `repos_index` and return details.

        The `repos_index` shape is flexible; this function will attempt to resolve
        dependency statuses from several common layouts:
          - { repo_name: { "task_details": { task_id: {"status": "done"} } } }
          - { task_id: "done" }
          - { task_id: {"status": "done"} }

        Returns a dict:
          {"ok": bool, "details": { dep_id: {"found": bool, "status": str|None, "repo": repo_name|None}}}

        The function is deterministic and logs exceptions rather than raising.
        """
        details: Dict[str, Any] = {}
        ok = True
        try:
            import yaml

            pm: Dict[str, Any] = {}
            if self.project_map_path.exists():
                pm = yaml.safe_load(self.project_map_path.read_text(encoding="utf-8")) or {}

            task = pm.get(task_id, {})
            deps = task.get("dependencies", []) if isinstance(task, dict) else []

            # No dependencies -> trivially satisfied
            if not deps:
                return {"ok": True, "details": {}, "message": "no dependencies"}

            # Helper to search repos_index for a dependency
            def find_dep(d: str) -> Tuple[bool, Optional[str], Optional[str]]:
                # direct mapping: repos_index.get(d)
                if isinstance(repos_index, dict) and d in repos_index:
                    v = repos_index[d]
                    if isinstance(v, str):
                        return True, v, None
                    if isinstance(v, dict) and "status" in v:
                        return True, v.get("status"), None

                # search repo entries for task_details
                if isinstance(repos_index, dict):
                    for repo_name, repo_val in repos_index.items():
                        if not isinstance(repo_val, dict):
                            continue
                        td = repo_val.get("task_details") or repo_val.get("tasks") or {}
                        if isinstance(td, dict) and d in td:
                            entry = td[d]
                            if isinstance(entry, str):
                                return True, entry, repo_name
                            if isinstance(entry, dict) and "status" in entry:
                                return True, entry.get("status"), repo_name
                # not found
                return False, None, None

            for d in deps:
                found, status, repo = find_dep(d)
                ok_dep = found and (status == "done")
                details[d] = {"found": found, "status": status, "repo": repo, "satisfied": bool(ok_dep)}
                if not ok_dep:
                    ok = False

        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("check_dependencies failed: %s", exc)
            return {"ok": False, "details": {}, "error": str(exc)}

        return {"ok": bool(ok), "details": details}

    # Placeholder methods for the rest of the PHASE 2 features. Implemented later.
    def scoring_loop(self):
        """Primary scoring loop.

        Reads `project_map.yml`, `scoring_kpis.yml`, and `task_contract.yml` when present
        and computes a deterministic per-task score and detailed metrics.

        Returns a dict mapping `task_id` -> result object containing:
          - metrics: raw KPI values
          - pre_gate_score: weighted score before gates
          - post_gate_score: weighted score after gates
          - final_score: post_gate_score * task_type_weight
          - details: diagnostic metadata
        """
        results: Dict[str, Any] = {}
        try:
            import yaml

            pm = {}
            sk = {}
            tc = {}
            if self.project_map_path.exists():
                pm = yaml.safe_load(self.project_map_path.read_text(encoding="utf-8")) or {}
            if self.scoring_kpis_path.exists():
                sk = yaml.safe_load(self.scoring_kpis_path.read_text(encoding="utf-8")) or {}
            if self.task_contract_path.exists():
                tc = yaml.safe_load(self.task_contract_path.read_text(encoding="utf-8")) or {}

            # canonical default weights (implementation-focused). User values override these.
            default_weights = {
                "STRUCTURAL_COMPLETENESS": 25,
                "IMPLEMENTATION_COMPLETENESS": 25,
                "PIPELINE_STAGE_COMPLETENESS": 10,
                "VALIDATOR_COMPLETENESS": 10,

                "CODE_ARTIFACT_PRESENT": 10,
                "TESTS_PASS": 10,
                "SPEC_COVERAGE": 5,
                "COMPLEXITY_PROFILE": 3,
                "DOCUMENTATION": 2,
            }
            # If user provides explicit score_weights, use them as authoritative
            # (do not merge with defaults). Otherwise fall back to canonical defaults.
            user_sw = sk.get("score_weights", None)
            if isinstance(user_sw, dict) and user_sw:
                score_weights = {}
                for k, v in user_sw.items():
                    try:
                        score_weights[str(k)] = float(v)
                    except Exception:
                        score_weights[str(k)] = v
            else:
                score_weights = dict(default_weights)

            task_type_weights = sk.get("task_type_weights", {})
            # gates may be represented as a dict mapping KPI->cap (preferred),
            # or as a list of KPI names (legacy). Normalize to gate_caps mapping.
            raw_gates = sk.get("gates", {})
            gate_caps: Dict[str, int] = {}
            if isinstance(raw_gates, dict):
                # explicit mapping: {"TESTS_PASS": 50}
                gate_caps = {k: int(v) for k, v in raw_gates.items()}
            elif isinstance(raw_gates, list):
                # legacy list -> default cap 50
                gate_caps = {k: 50 for k in raw_gates}

            # Sanity gate: if the repository-level sanity checks fail, we must not
            # compute numeric scores. Instead return a sentinel indicating we are
            # UNABLE_TO_SCORE as required by the PIL spec.
            sanity = self.run_sanity_gate()
            if not sanity.get("healthy", False):
                return {
                    "status": "UNABLE_TO_SCORE",
                    "explanation": "Repository sanity checks failed",
                    "sanity": sanity.get("details", {}),
                }

            # Precompute repository-level expected signals used by IMPLEMENTATION_COMPLETENESS
            try:
                repo_expected_pipeline_stages = sum(1 for t, e in (pm.items()) if isinstance(e, dict) and e.get("task_type") == "pipeline_stage")
                repo_expected_validators = sum(1 for t, e in (pm.items()) if isinstance(e, dict) and (e.get("validation_artifacts") or []))
            except Exception:
                repo_expected_pipeline_stages = 0
                repo_expected_validators = 0

            # compute median of functions+classes per python file across the repo
            repo_median_combined = 0
            try:
                import statistics

                counts: List[int] = []
                for p in self._gather_python_files():
                    try:
                        src = p.read_text(encoding="utf-8")
                        tree = ast.parse(src)
                    except Exception:
                        continue
                    fcount = 0
                    ccount = 0
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            fcount += 1
                        if isinstance(node, ast.ClassDef):
                            ccount += 1
                    counts.append(fcount + ccount)
                if counts:
                    repo_median_combined = int(statistics.median(counts))
                else:
                    repo_median_combined = 0
            except Exception:
                repo_median_combined = 0

            for task_id, task_entry in sorted(pm.items()):
                entry = task_entry or {}
                declared_impl_files = [str((self.repo_path / p).resolve()) for p in entry.get("implementation_files", []) if isinstance(p, str)]
                val_artifacts = entry.get("validation_artifacts", []) or []

                # Discover inferred implementation files under src/ when declared
                # files are missing, empty, or incomplete. The discovered files
                # are deduplicated against declared_impl_files.
                inferred_impl_files = self.discover_impl_files(declared_impl_files)

                # combine declared + inferred for actual scanning scope
                used_impl_files: List[str] = []
                # include declared resolved files that exist
                for f in declared_impl_files:
                    try:
                        if Path(f).exists():
                            used_impl_files.append(f)
                    except Exception:
                        continue
                # supplement with inferred files (deduped by discover_impl_files)
                for f in inferred_impl_files:
                    if f not in used_impl_files:
                        used_impl_files.append(f)

                # ------------------ Implementation-first KPIs & signals ------------------
                # gather repo-level structure once (prefer passing used impl files)
                structure_signals = self.scan_structure(pm, impl_files=used_impl_files)

                # per-task implementation signals (scan both declared and inferred)
                impl_signals = self.scan_implementation_signals(used_impl_files, task_id)

                # CODE_ARTIFACT_PRESENT: prefer declared files; else infer from code
                if used_impl_files:
                    exist_status = [self.calculate_artifact_hash(f) != MISSING_FILE_HASH for f in used_impl_files]
                    if all(exist_status):
                        code_k = 1.0
                    else:
                        # declared but missing or partially present -> neutral (do not penalize)
                        code_k = 0.5
                else:
                    # infer from codebase: if any module/function matches task -> 1.0, else 0.5 (unknown)
                    if impl_signals.get("modules_found", 0) > 0 or impl_signals.get("functions_found", 0) > 0:
                        code_k = 1.0
                    else:
                        code_k = 0.5

                # Targeted test aggregation
                test_results = self.parse_junit_reports()

                def artifact_tests_kpi(a: str) -> float:
                    # if a specific test case is referenced
                    if "::" in a:
                        filepart, testname = a.split("::", 1)
                        key = f"{filepart}::{testname}"
                        if key in test_results:
                            return 1.0 if test_results.get(key) else 0.0
                        # try matching any key that ends with ::testname
                        for k, v in test_results.items():
                            if k.endswith(f"::{testname}"):
                                return 1.0 if v else 0.0
                        # targeted tests referenced but not present -> uncertain
                        # Treat missing explicit referenced tests as partial evidence
                        # (0.5) rather than definitive failure (0.0)
                        return 0.5

                    # file-level artifact e.g. tests/foo.py
                    if isinstance(a, str) and a.endswith(".py"):
                        found_any = False
                        for k, v in test_results.items():
                            if k.startswith(a) or k.split("::")[0].endswith(a):
                                found_any = True
                                if v:
                                    return 1.0
                                else:
                                    return 0.0
                        # targeted tests do not exist -> uncertain (0.5)
                        return 0.5

                    return 0.5

                tests_required = [a for a in val_artifacts if ("::" in a) or (isinstance(a, str) and a.endswith(".py"))]
                if tests_required:
                    # aggregate: if any referenced test fails -> 0.0, if all pass ->1.0, if some missing ->0.5
                    vals = [artifact_tests_kpi(a) for a in tests_required]
                    if all(v == 1.0 for v in vals):
                        tests_k = 1.0
                    elif any(v == 0.0 for v in vals) and not all(v == 1.0 for v in vals):
                        # if any explicit referenced test failed -> 0.0
                        tests_k = 0.0
                    else:
                        tests_k = 0.5
                else:
                    tests_k = 0.5

                # SPEC_COVERAGE -> convert percent to [0.0..1.0]; missing metadata => neutral
                spec_coverage = self.compute_spec_coverage(entry)
                spec_k = max(0.0, min(1.0, float(spec_coverage) / 100.0))

                # COMPLEXITY_PROFILE -> replaced by implementation richness heuristic
                # Allow complexity weights/thresholds to be configured via scoring_kpis.yml
                complexity_cfg = {}
                try:
                    complexity_cfg = sk.get("complexity", {}) if isinstance(sk, dict) else {}
                except Exception:
                    complexity_cfg = {}

                complexity_score, complexity_details = self.compute_complexity_profile(used_impl_files, complexity_cfg)
                # New bucketization: thresholds configurable via complexity_cfg["thresholds"] or fall back to defaults
                thresholds = (complexity_cfg or {}).get("thresholds", {})
                high_t = int(thresholds.get("high", 70))
                mid_t = int(thresholds.get("mid", 30))
                if complexity_score >= high_t:
                    comp_k = 1.0
                elif complexity_score >= mid_t:
                    comp_k = 0.5
                else:
                    comp_k = 0.0

                # Implementation-first override: strong implementation signals
                # (multiple functions or detected pipeline stages) should
                # elevate complexity KPI to fully satisfied so progress
                # reflects real implementation work rather than strict
                # numeric thresholds alone.
                try:
                    if impl_signals.get("functions_found", 0) >= 2 or impl_signals.get("pipeline_stages_detected", 0) > 0:
                        comp_k = 1.0
                except Exception:
                    pass

                # DOCUMENTATION -> detect README, docs, or inline docstrings
                doc_k = 0.5
                if (self.repo_path / "README.md").exists() or (self.repo_path / "docs").exists():
                    doc_k = 1.0
                else:
                    # inspect implementation files for docstrings
                    try:
                        for p in self._gather_python_files():
                            try:
                                src = p.read_text(encoding="utf-8")
                                tree = ast.parse(src)
                                for node in tree.body:
                                    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                                        if ast.get_docstring(node):
                                            doc_k = 1.0
                                            break
                                if doc_k == 1.0:
                                    break
                            except Exception:
                                continue
                    except Exception:
                        doc_k = 0.5

                # New KPIs (implementation-first): STRUCTURAL, IMPLEMENTATION, PIPELINE, VALIDATOR
                struct_pct = structure_signals.get("percent_structure_complete", 0)
                if struct_pct >= 80:
                    struct_k = 1.0
                elif struct_pct >= 50:
                    struct_k = 0.5
                else:
                    struct_k = 0.0

                # If declared implementation files are missing (empty list) but
                # code exists (we have inferred or used impl files), ensure we
                # do not drop STRUCTURAL_COMPLETENESS below neutral (0.5).
                declared_missing = (len(declared_impl_files) == 0)
                code_present = bool(used_impl_files)
                if declared_missing and code_present and struct_k < 0.5:
                    struct_k = 0.5

                # IMPLEMENTATION_COMPLETENESS (task-level)
                # Use combined signals from declared + inferred files.
                detected_functions = impl_signals.get("functions_found", 0)
                detected_classes = impl_signals.get("classes_found", 0)
                detected_stages = impl_signals.get("pipeline_stages_detected", 0)
                detected_validators = impl_signals.get("validators_detected", 0)

                # Pipeline completeness relative to repo expected (use helper)
                pipeline_score = self.compute_pipeline_stage_completeness(
                    repo_expected_pipeline_stages,
                    detected_stages,
                    impl_signals,
                    repo_median_combined,
                    complexity_score,
                )

                # Validator completeness relative to repo expected (use helper)
                validator_score = self.compute_validator_subscore(repo_expected_validators, detected_validators)

                # Functions/classes completeness relative to median across repo
                rich = self.compute_rich_implementation_signals(impl_signals, repo_median_combined, complexity_score)
                fc_score = rich.get("fc_score", 0.5)

                # Combine sub-scores to form IMPLEMENTATION_COMPLETENESS.
                # The KPI must be one of the canonical buckets {0.0, 0.5, 1.0}.
                raw_impl = float((pipeline_score + validator_score + fc_score) / 3.0)
                if raw_impl >= 0.75:
                    impl_k = 1.0
                elif raw_impl >= 0.25:
                    impl_k = 0.5
                else:
                    impl_k = 0.0

                # PIPELINE_STAGE_COMPLETENESS
                expected_pipeline_stages = sum(1 for t, e in (pm.items()) if isinstance(e, dict) and e.get("task_type") == "pipeline_stage")
                detected_stages = impl_signals.get("pipeline_stages_detected", 0)
                pipeline_k = self.compute_pipeline_stage_completeness(
                    expected_pipeline_stages, detected_stages, impl_signals, repo_median_combined, complexity_score
                )

                # VALIDATOR_COMPLETENESS (task-level KPI)
                validator_k = self.compute_validator_kpi(val_artifacts, impl_signals.get("validators_detected", 0))

                # STATE_TRANSITION -> only detect/enforce when listed in done_contract or scored
                # Determine done_contract entries per task
                # NOTE: per canonical behavior, only honor `done_contract` when
                # explicitly provided in the task's `project_map` entry. Do NOT
                # inherit or fall back to repository-level `task_contract.yml`.
                done_contract_entries = []
                if isinstance(entry.get("done_contract"), list):
                    done_contract_entries = entry.get("done_contract")

                # compute state detection if the task explicitly requires it via
                # `done_contract` OR if `STATE_TRANSITION` is present in the
                # configured `score_weights`. This preserves compatibility with
                # tests that assert detection when the KPI is being scored.
                state_required = any(d == "state_transition_implemented" for d in (done_contract_entries or [])) or (isinstance(score_weights, dict) and ("STATE_TRANSITION" in score_weights))
                if state_required:
                    state_ok, state_details = self.check_state_transition_implemented(used_impl_files)
                    state_k = 1.0 if state_ok else 0.0
                else:
                    state_k = None

                # SANITY_GATE is guaranteed above to be healthy (we returned early otherwise), so set to 1.0
                sanity_k = 1.0

                # Build KPI map with None for not-applicable
                metrics_k = {
                    # Implementation-first KPIs
                    "STRUCTURAL_COMPLETENESS": struct_k,
                    "IMPLEMENTATION_COMPLETENESS": impl_k,
                    "PIPELINE_STAGE_COMPLETENESS": pipeline_k,
                    "VALIDATOR_COMPLETENESS": validator_k,

                    # Code & tests
                    "CODE_ARTIFACT_PRESENT": code_k,
                    "TESTS_PASS": tests_k,
                    "SPEC_COVERAGE": spec_k,
                    "COMPLEXITY_PROFILE": comp_k,
                    "DOCUMENTATION": doc_k,

                    # Other
                    "SANITY_GATE": sanity_k,
                    "STATE_TRANSITION": state_k,
                }

                # ------------------ done_contract enforcement (no hard zeros) ------------------
                # Map done_contract names to KPI metric keys
                done_to_kpi = {
                    "implementation_files_present": "CODE_ARTIFACT_PRESENT",
                    "tests_pass": "TESTS_PASS",
                    "state_transition_implemented": "STATE_TRANSITION",
                    "dependency_fulfilled": "DEPENDENCY_FULFILLED",
                }

                required_kpis: List[str] = []
                for d in (done_contract_entries or []):
                    if isinstance(d, str) and d in done_to_kpi:
                        required_kpis.append(done_to_kpi[d])

                # compute pre-gate weighted score (weights are percentages)
                total_weight = sum(float(v) for v in score_weights.values()) if score_weights else 100.0
                weighted = 0.0
                # iterate over configured score_weights only
                for k, w in (score_weights.items() if score_weights else {}):
                    try:
                        wv = float(w)
                    except Exception:
                        wv = 0.0
                    mv = metrics_k.get(k)
                    if mv is None:
                        # KPI not applicable for this task -> treat as neutral (0.5)
                        mv_val = 0.5
                    else:
                        mv_val = float(mv)
                    weighted += (wv * mv_val)

                pre_gate_score = int(round((weighted / total_weight) * 100.0))

                # --- Split scores: progress vs compliance ---
                # Allow KPI grouping configuration via scoring_kpis.yml
                # Progress KPIs are strictly implementation-focused. Per
                # specification progress_score must be computed only from
                # implementation signals and tests evidence.
                default_progress = [
                    "STRUCTURAL_COMPLETENESS",
                    "IMPLEMENTATION_COMPLETENESS",
                    "PIPELINE_STAGE_COMPLETENESS",
                    "VALIDATOR_COMPLETENESS",
                    "COMPLEXITY_PROFILE",
                    "TESTS_PASS",
                ]

                # Compliance KPIs are policy/metadata oriented.
                default_compliance = [
                    "SPEC_COVERAGE",
                    "DOCUMENTATION",
                    "SANITY_GATE",
                    "STATE_TRANSITION",
                ]

                kpi_groups = (sk or {}).get("kpi_groups", {}) if isinstance(sk, dict) else {}
                progress_kpis = kpi_groups.get("progress", default_progress)
                compliance_kpis = kpi_groups.get("compliance", default_compliance)

                def compute_subset_score(kpi_list: List[str]) -> Tuple[int, float]:
                    total = 0.0
                    acc = 0.0
                    for k in kpi_list:
                        w = float(score_weights.get(k, 0.0))
                        total += w
                        mv = metrics_k.get(k)
                        mv_val = 0.5 if mv is None else float(mv)
                        acc += (w * mv_val)
                    if total <= 0.0:
                        return 0, 0.0
                    return int(round((acc / total) * 100.0)), total

                progress_pre, progress_total = compute_subset_score(progress_kpis)
                compliance_pre, compliance_total = compute_subset_score(compliance_kpis)

                # If both groups have zero configured weight (no KPIs in groups
                # intersect configured score_weights), fall back to using the
                # overall pre_gate_score for both to preserve expected legacy
                # behavior where a single configured KPI drives the total.
                if (progress_total <= 0.0) and (compliance_total <= 0.0):
                    progress_pre = pre_gate_score
                    compliance_pre = pre_gate_score

                # apply gates as caps to compliance only. Progress is strictly
                # derived from implementation signals and MUST NOT be reduced
                # by gates or compliance enforcement (implementation-first rule).
                progress_post = progress_pre
                compliance_post = compliance_pre
                for g, cap in gate_caps.items():
                    k_val = metrics_k.get(g)
                    if k_val is None:
                        continue
                    try:
                        capv = int(cap)
                    except Exception:
                        capv = 50
                    # Only apply caps to compliance group here
                    if g in compliance_kpis and float(k_val) < 1.0:
                        compliance_post = min(compliance_post, capv)

                # apply gates as caps using gate_caps mapping (overall)
                post_gate_score = pre_gate_score
                for g, cap in gate_caps.items():
                    # only evaluate gate if KPI is applicable
                    k_val = metrics_k.get(g)
                    if k_val is None:
                        # not applicable -> do not impose gate
                        continue
                    # gate applies when KPI is not fully satisfied
                    if float(k_val) < 1.0:
                        try:
                            capv = int(cap)
                        except Exception:
                            capv = 50
                        post_gate_score = min(post_gate_score, capv)

                # done_contract enforcement (metadata-neutral):
                # - Missing metadata (None) is treated as neutral and does NOT
                #   cause a hard failure.
                # - Only an explicit failing KPI value (0.0) forces a hard zero
                #   on the post_gate_score. Partial values (<1.0 but >0.0) will
                #   impose a conservative cap (default 50) instead of zero.
                required_failure_hard_zero = False
                if required_kpis:
                    for rk in required_kpis:
                        rv = metrics_k.get(rk)
                        try:
                            # missing metadata -> neutral (do not fail)
                            if rv is None:
                                continue
                            val = float(rv)
                            # explicit failure -> hard zero for compliance/post gate
                            if val == 0.0:
                                post_gate_score = 0
                                compliance_post = 0
                                # record that a required KPI explicitly failed
                                required_failure_hard_zero = True
                                break
                            # partial satisfaction -> conservative cap (50) on compliance and overall
                            if val < 1.0:
                                post_gate_score = min(post_gate_score, 50)
                                if rk in compliance_kpis:
                                    compliance_post = min(compliance_post, 50)
                        except Exception:
                            # parsing error -> treat as neutral
                            continue

                # finalize progress/compliance combined score
                # allow weighting via scoring_kpis.yml: group_weights: {progress: n, compliance: m}
                group_weights = (sk or {}).get("group_weights", {}) if isinstance(sk, dict) else {}
                try:
                    pw = float(group_weights.get("progress", 1.0))
                except Exception:
                    pw = 1.0
                try:
                    cw = float(group_weights.get("compliance", 1.0))
                except Exception:
                    cw = 1.0
                denom = pw + cw if (pw + cw) != 0 else 1.0
                combined_post = int(round((float(progress_post) * pw + float(compliance_post) * cw) / denom))

                # If any required KPI explicitly failed (hard zero), enforce
                # a hard zero on the combined outcome as well while keeping
                # the `progress_score` intact. This allows progress to reflect
                # implementation signals while ensuring final outcomes respect
                # done_contract enforcement.
                if required_failure_hard_zero:
                    combined_post = 0

                # finalize task_type and final_score multiplier
                task_type = "pipeline_stage"
                if isinstance(entry.get("task_type"), str):
                    task_type = entry.get("task_type")
                else:
                    if any(p.startswith("docs/") for p in entry.get("implementation_files", []) if isinstance(p, str)):
                        task_type = "documentation"

                type_mult = float(task_type_weights.get(task_type, 1.0))
                final_score = int(round(combined_post * type_mult))

                # prepare metrics for output. Map None -> neutral (0.5) so
                # missing metadata or not-applicable KPIs do not penalize progress.
                out_metrics = {}
                for k, v in metrics_k.items():
                    if v is None:
                        out_metrics[k] = 0.5
                    elif isinstance(v, float):
                        # represent numeric KPI values as floats (0.0, 0.5, 1.0)
                        out_metrics[k] = float(v)
                    else:
                        out_metrics[k] = v

                results[task_id] = {
                    "metrics": out_metrics,
                    "pre_gate_score": pre_gate_score,
                    "post_gate_score": post_gate_score,
                    "progress_score": int(progress_post),
                    "compliance_score": int(compliance_post),
                    "combined_score": int(combined_post),
                    "final_score": final_score,
                    "task_type": task_type,
                    "details": {
                        "declared_impl_files": declared_impl_files,
                        "inferred_impl_files": inferred_impl_files,
                        "impl_files": used_impl_files,
                        "validation_artifacts": val_artifacts,
                        "implementation_signals": impl_signals,
                        "percent_structure_complete": structure_signals.get("percent_structure_complete"),
                        "complexity_details": complexity_details,
                    },
                }

        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("scoring_loop failed: %s", exc)

        return results

    def compute_spec_coverage(self, entry: Dict[str, Any]) -> int:
        """Compute spec coverage percentage from a `project_map` task entry.

        Returns integer percentage in [0,100]. If no coverage entries present, returns 0.
        """
        if not isinstance(entry, dict):
            # no entry -> uncertain by default
            return 50
        spec_cov_entries = entry.get("task_spec_coverage", []) or []
        if not spec_cov_entries:
            # missing or empty coverage entries -> treat as uncertain (50%)
            return 50
        covered = 0
        total = 0
        for s in spec_cov_entries:
            if isinstance(s, dict) and "covered" in s:
                total += 1
                if bool(s.get("covered")):
                    covered += 1
        if total == 0:
            return 50
        return int((covered / total) * 100)

    def compute_complexity_profile(self, impl_files: List[str], config: Optional[Dict[str, Any]] = None) -> Tuple[int, Dict[str, Any]]:
        """Compute an implementation-richness heuristic and return (score, details).

        The heuristic is based on:
          - pipeline_stage_count
          - validator_count
          - adapter_count
          - module_depth (max directory depth)
          - function/class count

        Returns (score 0..100, details dict).
        """
        # If specific implementation files were provided, limit analysis to them.
        py_files: List[Path] = []
        if impl_files:
            seen = set()
            for f in impl_files:
                try:
                    p = Path(f)
                    if not p.is_absolute():
                        p = (self.repo_path / p).resolve()
                    else:
                        p = p.resolve()
                except Exception:
                    # fallback: join with repo_path
                    p = (self.repo_path / Path(f)).resolve()
                if p.exists() and p.suffix == ".py":
                    if str(p) not in seen:
                        seen.add(str(p))
                        py_files.append(p)
        else:
            py_files = self._gather_python_files()

        # Aggregate raw counts for the provided impl_files
        func_count = 0
        class_count = 0
        pipeline_stage_count = 0
        validator_count = 0
        adapter_count = 0
        max_depth = 0

        for p in py_files:
            try:
                rel = p.relative_to(self.repo_path)
            except Exception:
                rel = p
            depth = len(rel.parts) - 1
            if depth > max_depth:
                max_depth = depth
            try:
                src = p.read_text(encoding="utf-8")
                tree = ast.parse(src)
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_count += 1
                    name = node.name.lower()
                    if "stage" in name or "pipeline" in name or any((isinstance(d, ast.Name) and "stage" in d.id.lower()) or (isinstance(d, ast.Attribute) and "stage" in getattr(d, "attr", "").lower()) for d in node.decorator_list):
                        pipeline_stage_count += 1
                    # validator by name
                    if "validate" in name:
                        validator_count += 1
                if isinstance(node, ast.ClassDef):
                    class_count += 1
                    name = node.name.lower()
                    if "validator" in name or "validate" in name:
                        validator_count += 1
                    if "adapter" in name:
                        adapter_count += 1
                if isinstance(node, ast.Call):
                    fn = node.func
                    fname = None
                    if isinstance(fn, ast.Name):
                        fname = fn.id.lower()
                    elif isinstance(fn, ast.Attribute):
                        fname = getattr(fn, "attr", "").lower()
                    if fname and ("validate" in fname or "schema" in fname):
                        validator_count += 1

            # file-level module name based validators detection
            try:
                if p.name.lower() == "validators.py" or p.name.lower().endswith("_validators.py"):
                    validator_count += 1
            except Exception:
                pass

        # Repo-level totals for normalization (min-max scaling across repository)
        repo_py = self._gather_python_files()
        repo_totals = {
            "functions": 0,
            "classes": 0,
            "pipeline_stages": 0,
            "validators": 0,
            "adapters": 0,
            "module_depth": 0,
        }
        for rp in repo_py:
            try:
                rsrc = rp.read_text(encoding="utf-8")
                rtree = ast.parse(rsrc)
            except Exception:
                continue
            rfunc = 0
            rclass = 0
            rpipe = 0
            rval = 0
            radapt = 0
            try:
                rrel = rp.relative_to(self.repo_path)
                rdepth = len(rrel.parts) - 1
            except Exception:
                rdepth = 0
            if rdepth > repo_totals["module_depth"]:
                repo_totals["module_depth"] = rdepth
            for node in ast.walk(rtree):
                if isinstance(node, ast.FunctionDef):
                    rfunc += 1
                    rname = node.name.lower()
                    if "stage" in rname or "pipeline" in rname or any((isinstance(d, ast.Name) and "stage" in d.id.lower()) or (isinstance(d, ast.Attribute) and "stage" in getattr(d, "attr", "").lower()) for d in node.decorator_list):
                        rpipe += 1
                    if "validate" in rname:
                        rval += 1
                if isinstance(node, ast.ClassDef):
                    rclass += 1
                    rname = node.name.lower()
                    if "validator" in rname or "validate" in rname:
                        rval += 1
                    if "adapter" in rname:
                        radapt += 1
                if isinstance(node, ast.Call):
                    rf = node.func
                    rfname = None
                    if isinstance(rf, ast.Name):
                        rfname = rf.id.lower()
                    elif isinstance(rf, ast.Attribute):
                        rfname = getattr(rf, "attr", "").lower()
                    if rfname and ("validate" in rfname or "schema" in rfname):
                        rval += 1
            repo_totals["functions"] += rfunc
            repo_totals["classes"] += rclass
            repo_totals["pipeline_stages"] += rpipe
            repo_totals["validators"] += rval
            repo_totals["adapters"] += radapt

        # Prevent division by zero: use 1 as denominator if totals are zero
        denom_funcs = repo_totals["functions"] or 1
        denom_classes = repo_totals["classes"] or 1
        denom_pipeline = repo_totals["pipeline_stages"] or 1
        denom_validators = repo_totals["validators"] or 1
        denom_adapters = repo_totals["adapters"] or 1
        denom_depth = repo_totals["module_depth"] or 1

        # Scale each metric to 0..100 using min-max (min assumed 0)
        scaled_funcs = int(min(100, round((func_count / denom_funcs) * 100.0)))
        scaled_classes = int(min(100, round((class_count / denom_classes) * 100.0)))
        scaled_pipeline = int(min(100, round((pipeline_stage_count / denom_pipeline) * 100.0)))
        scaled_validators = int(min(100, round((validator_count / denom_validators) * 100.0)))
        scaled_adapters = int(min(100, round((adapter_count / denom_adapters) * 100.0)))
        scaled_depth = int(min(100, round((max_depth / denom_depth) * 100.0)))

        # Combine scaled metrics with weights (sum weights = 100)
        # Allow overriding weights via config: config["weights"] = {"pipeline":30,...}
        cfg_weights = (config or {}).get("weights", {}) if isinstance(config, dict) else {}
        def wget(k, default):
            try:
                v = int(cfg_weights.get(k))
                return v
            except Exception:
                return default

        w_pipeline = wget("pipeline", 30)
        w_validators = wget("validators", 25)
        w_funcs = wget("functions", 15)
        w_classes = wget("classes", 10)
        w_adapters = wget("adapters", 10)
        w_depth = wget("depth", 10)

        total_w = float(w_pipeline + w_validators + w_funcs + w_classes + w_adapters + w_depth)
        weighted_sum = (
            scaled_pipeline * w_pipeline
            + scaled_validators * w_validators
            + scaled_funcs * w_funcs
            + scaled_classes * w_classes
            + scaled_adapters * w_adapters
            + scaled_depth * w_depth
        )

        score = int(min(100, round(weighted_sum / total_w)))

        details = {
            "pipeline_stage_count": pipeline_stage_count,
            "validator_count": validator_count,
            "adapter_count": adapter_count,
            "function_count": func_count,
            "class_count": class_count,
            "module_depth": max_depth,
            "scaled": {
                "pipeline_stage": scaled_pipeline,
                "validators": scaled_validators,
                "adapters": scaled_adapters,
                "functions": scaled_funcs,
                "classes": scaled_classes,
                "module_depth": scaled_depth,
            },
            "repo_totals": repo_totals,
        }
        return score, details

    # ------------------------ Heuristic helper functions ------------------
    def compute_rich_implementation_signals(self, impl_signals: Dict[str, int], repo_median_combined: int, complexity_score: int) -> Dict[str, Any]:
        """Derive higher-level implementation signals from raw counts.

        Returns a dict containing:
          - 'combined_detected': int (functions + classes)
          - 'strong_impl': bool (true when evidence indicates strong implementation)
          - 'fc_score': float in {0.0,0.5,1.0} based on combined_detected vs repo_median_combined

        This helper centralizes the logic used by pipeline and implementation
        completeness computations to make behavior explicit and testable.
        """
        funcs = int(impl_signals.get("functions_found", 0))
        classes = int(impl_signals.get("classes_found", 0))
        combined = funcs + classes

        # fc_score: bucketized relative to repo median baseline
        if repo_median_combined > 0:
            if combined >= repo_median_combined:
                fc_score = 1.0
            elif combined >= (repo_median_combined / 2.0):
                fc_score = 0.5
            else:
                fc_score = 0.0
        else:
            fc_score = 0.5

        # strong_impl heuristic: either meets/exceeds median OR complexity is high
        try:
            strong_impl = combined >= max(1, repo_median_combined) or (complexity_score and complexity_score >= 50)
        except Exception:
            strong_impl = combined >= 1

        return {
            "combined_detected": combined,
            "strong_impl": bool(strong_impl),
            "fc_score": float(fc_score),
        }

    def compute_pipeline_stage_completeness(self, expected_pipeline_stages: int, detected_stages: int, impl_signals: Dict[str, int], repo_median_combined: int, complexity_score: int) -> float:
        """Compute the pipeline stage completeness KPI (0.0, 0.5, 1.0).

        Behavior:
        - If `expected_pipeline_stages` > 0: prefer direct detections (detected_stages);
          fall back to using `strong_impl` evidence to avoid penalizing implementation-heavy repos.
        - If no expected stages (expected_pipeline_stages == 0) -> neutral (0.5).
        """
        if expected_pipeline_stages > 0:
            if detected_stages >= expected_pipeline_stages:
                return 1.0
            if detected_stages >= (expected_pipeline_stages / 2.0):
                return 0.5

            # fallback: if strong implementation evidence exists, treat as satisfied
            rich = self.compute_rich_implementation_signals(impl_signals, repo_median_combined, complexity_score)
            return 1.0 if rich.get("strong_impl") else 0.0
        else:
            return 0.5

    def compute_validator_subscore(self, repo_expected_validators: int, detected_validators: int) -> float:
        """Compute validator sub-score used inside IMPLEMENTATION_COMPLETENESS.

        Relative to repo-level expectations; buckets into 0.0/0.5/1.0.
        """
        if repo_expected_validators > 0:
            if detected_validators >= repo_expected_validators:
                return 1.0
            if detected_validators >= (repo_expected_validators / 2.0):
                return 0.5
            return 0.0
        return 0.5

    def compute_validator_kpi(self, val_artifacts: List[str], detected_validators: int) -> float:
        """Compute the VALIDATOR_COMPLETENESS KPI for task-level reporting.

        - If the task declares validation artifacts: absence of validators -> 0.0.
        - If none declared: neutral (0.5).
        """
        if val_artifacts:
            return 1.0 if detected_validators > 0 else 0.0
        return 0.5

if __name__ == "__main__":
    # Simple smoke exercise when executed directly (no side effects)
    scanner = PILScanner(repo_path=".")
    sanity = scanner.run_sanity_gate()
    print(json.dumps(sanity, indent=2))
def aggregate_all_repos(repo_list: List[str], include_timestamps: bool = False) -> Dict[str, Any]:
    """Aggregate results from multiple repositories into a master `repos_index`.

    The returned mapping uses the repository directory name as the top-level key.
    For each repo we include: `repo_path`, `tasks` (task_id -> status + score),
    `scoring` (detailed per-task results), `deltas` (version/delta info), and
    `dependencies` (per-task dependency checks).

    Deterministic rules:
      - A task is considered `done` if `final_score >= 80`, otherwise `pending`.
      - Dependencies are checked against the aggregated `repos_index` built so far
        which allows inter-repo references to be resolved deterministically.
    """
    aggregated: Dict[str, Any] = {}
    # Build incrementally so dependencies can resolve previously-seen repos
    for repo_path in repo_list:
        scanner = PILScanner(repo_path)
        repo_name = str(Path(repo_path).resolve().name)
        scoring = scanner.scoring_loop()
        deltas = scanner.version_and_drift_detection()
        # handle UNABLE_TO_SCORE sentinel returned by scoring_loop
        tasks_summary: Dict[str, Any] = {}
        deps_results: Dict[str, Any] = {}
        if isinstance(scoring, dict) and scoring.get("status") == "UNABLE_TO_SCORE":
            # record sanity details and skip task-level scoring
            aggregated[repo_name] = {
                "repo_path": str(Path(repo_path).resolve()),
                "status": scoring.get("status"),
                "explanation": scoring.get("explanation"),
                "sanity": scoring.get("sanity"),
                "scoring": {},
                "deltas": deltas,
                "dependencies": {},
            }
            # continue to next repo (no task-level dependency checks possible)
            continue

        # compute task status summary for normal scoring results
        for tid, res in scoring.items():
            final = int(res.get("final_score", 0))
            status = "done" if final >= 80 else "pending"
            tasks_summary[tid] = {"final_score": final, "status": status}

        # check dependencies for each task against current aggregated index
        for tid in scoring.keys():
            deps_results[tid] = scanner.check_dependencies(tid, aggregated)

        aggregated[repo_name] = {
            "repo_path": str(Path(repo_path).resolve()),
            "tasks": tasks_summary,
            "scoring": scoring,
            "deltas": deltas,
            "dependencies": deps_results,
        }
        # optional timestamps: derive last-mod times for implementation files and test reports
        if include_timestamps:
            try:
                all_times = []
                for tid, res in scoring.items():
                    for f in res.get("details", {}).get("impl_files", []) or []:
                        try:
                            t = Path(f).stat().st_mtime
                            all_times.append(float(t))
                        except Exception:
                            continue
                # include test-reports modification times
                tr = Path(repo_path) / "test-reports"
                if tr.exists():
                    for p in tr.glob("*.xml"):
                        try:
                            all_times.append(float(p.stat().st_mtime))
                        except Exception:
                            continue
                if all_times:
                    aggregated[repo_name]["artifact_age"] = {"last_mod_epoch": int(max(all_times)), "source": "mtime"}
                else:
                    aggregated[repo_name]["artifact_age"] = {"last_mod_epoch": None, "source": None}
            except Exception:
                aggregated[repo_name]["artifact_age"] = {"last_mod_epoch": None, "source": "error"}

    return aggregated


def save_repos_index(repos_index: Dict[str, Any], out_path: str) -> None:
    """Serialize `repos_index` to YAML at `out_path` using deterministic ordering.

    If `yaml` is not available the function writes JSON as a fallback.
    """
    try:
        import yaml

        with open(out_path, "w", encoding="utf-8") as fh:
            # sort keys for deterministic output
            yaml.safe_dump(repos_index, fh, sort_keys=True)
    except Exception:
        # fallback to JSON
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(repos_index, fh, sort_keys=True, indent=2)


def _make_sparkline(values: List[float]) -> str:
    """Create a small block-character sparkline string from numeric `values`.

    Maps values (0..100) into 8-level blocks: ▁▂▃▄▅▆▇█.
    """
    blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    out = []
    for v in values:
        try:
            x = float(v)
        except Exception:
            x = 0.0
        idx = int(min(7, max(0, round((x / 100.0) * 7))))
        out.append(blocks[idx])
    return "".join(out)


def save_repos_index_with_history(repos_index: Dict[str, Any], out_path: str, history_len: int = 20) -> None:
    """Save `repos_index` while preserving and updating per-repo progress history.

    Behavior:
      - If `out_path` exists and is YAML/JSON, attempts to load previous history per repo.
      - Appends the current average final_score for each repo to its history (capped by `history_len`).
      - Adds `progress_history_values` (list) and `progress_history` (sparkline) to each repo entry.
    """
    prev = {}
    try:
        import yaml

        if os.path.exists(out_path):
            try:
                with open(out_path, "r", encoding="utf-8") as fh:
                    prev = yaml.safe_load(fh) or {}
            except Exception:
                prev = {}
    except Exception:
        # attempt JSON load
        if os.path.exists(out_path):
            try:
                with open(out_path, "r", encoding="utf-8") as fh:
                    prev = json.load(fh) or {}
            except Exception:
                prev = {}

    # compute current averages and merge
    for repo_name, repo_data in repos_index.items():
        scoring = repo_data.get("scoring", {}) or {}
        # average final_score across tasks
        scores = []
        for tid, res in scoring.items():
            try:
                scores.append(float(res.get("final_score", 0)))
            except Exception:
                scores.append(0.0)
        avg = float(sum(scores) / len(scores)) if scores else 0.0

        prev_repo = prev.get(repo_name, {}) if isinstance(prev, dict) else {}
        prev_vals = prev_repo.get("progress_history_values") if isinstance(prev_repo, dict) else None
        if not isinstance(prev_vals, list):
            prev_vals = []
        new_vals = prev_vals + [avg]
        # cap length
        if len(new_vals) > history_len:
            new_vals = new_vals[-history_len:]

        # attach to repo_data
        repo_data["progress_history_values"] = [float(x) for x in new_vals]
        repo_data["progress_history"] = _make_sparkline(repo_data["progress_history_values"])

    # finally persist using existing save function (yaml preferred)
    try:
        import yaml

        with open(out_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(repos_index, fh, sort_keys=True)
    except Exception:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(repos_index, fh, sort_keys=True, indent=2)
