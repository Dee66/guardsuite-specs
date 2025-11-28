import runpy
import os
import yaml
from pathlib import Path


def _load_scanner_module():
    base = os.path.dirname(__file__)
    modpath = os.path.join(base, "..", "repo-scanner.py")
    ns = runpy.run_path(modpath)
    return ns["PILScanner"]


def test_compute_rich_implementation_signals_strong():
    PILScanner = _load_scanner_module()
    s = PILScanner('.')
    impl_signals = {"functions_found": 10, "classes_found": 0}
    rich = s.compute_rich_implementation_signals(impl_signals, repo_median_combined=2, complexity_score=0)
    assert isinstance(rich, dict)
    assert rich["combined_detected"] == 10
    assert rich["strong_impl"] is True
    assert rich["fc_score"] == 1.0


def test_compute_rich_implementation_signals_weak():
    PILScanner = _load_scanner_module()
    s = PILScanner('.')
    impl_signals = {"functions_found": 0, "classes_found": 0}
    rich = s.compute_rich_implementation_signals(impl_signals, repo_median_combined=4, complexity_score=0)
    assert rich["combined_detected"] == 0
    assert rich["strong_impl"] is False
    assert rich["fc_score"] in (0.0, 0.5)


def test_compute_pipeline_stage_completeness_behaviour():
    PILScanner = _load_scanner_module()
    s = PILScanner('.')
    # expected stages >0, but none detected, strong impl -> satisfied
    impl_signals = {"functions_found": 5, "classes_found": 0}
    k = s.compute_pipeline_stage_completeness(expected_pipeline_stages=2, detected_stages=0, impl_signals=impl_signals, repo_median_combined=2, complexity_score=0)
    assert k == 1.0

    # expected stages >0, none detected, weak impl -> not satisfied
    impl_signals = {"functions_found": 0, "classes_found": 0}
    k2 = s.compute_pipeline_stage_completeness(expected_pipeline_stages=2, detected_stages=0, impl_signals=impl_signals, repo_median_combined=4, complexity_score=0)
    assert k2 == 0.0


def test_compute_validator_kpi():
    PILScanner = _load_scanner_module()
    s = PILScanner('.')
    # when validation artifacts declared and none detected -> 0.0
    v = s.compute_validator_kpi(["tests/foo.py"], detected_validators=0)
    assert v == 0.0
    # when none declared -> neutral
    v2 = s.compute_validator_kpi([], detected_validators=0)
    assert v2 == 0.5
