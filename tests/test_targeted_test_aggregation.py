from pathlib import Path
import yaml
import xml.etree.ElementTree as ET


def _write_junit_xml(path: Path, file: str, testname: str, passed: bool = True):
    testsuite = ET.Element("testsuite")
    tc = ET.SubElement(testsuite, "testcase", attrib={"name": testname, "file": file})
    if not passed:
        ET.SubElement(tc, "failure")
    tree = ET.ElementTree(testsuite)
    tree.write(str(path), encoding="utf-8", xml_declaration=True)


def test_targeted_test_aggregation(tmp_path):
    # repo layout
    repo = tmp_path
    tr = repo / "test-reports"
    tr.mkdir()

    # create junit xml with a passing testcase
    _write_junit_xml(tr / "report.xml", "tests/test_dummy.py", "test_ok", passed=True)

    # create project_map with validation_artifacts referencing that test
    project_map = {
        "T1": {
            "implementation_files": ["a.py"],
            "validation_artifacts": ["tests/test_dummy.py::test_ok"],
        }
    }

    (repo / "project_map.yml").write_text(yaml.safe_dump(project_map), encoding="utf-8")

    # write a minimal scoring_kpis.yml so scoring_loop loads
    scoring = {"score_weights": {"TESTS_PASS": 100}, "task_type_weights": {}}
    (repo / "scoring_kpis.yml").write_text(yaml.safe_dump(scoring), encoding="utf-8")

    # write implementation file
    (repo / "a.py").write_text("print('x')\n", encoding="utf-8")

    # run scanner
    import importlib.util

    spec = importlib.util.spec_from_file_location("repo_scanner", Path("repo-scanner.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    scanner = mod.PILScanner(str(repo))
    results = scanner.scoring_loop()

    assert "T1" in results
    # KPI values are numeric (0.0/0.5/1.0); expect fully passing -> 1.0
    assert results["T1"]["metrics"]["TESTS_PASS"] == 1.0
