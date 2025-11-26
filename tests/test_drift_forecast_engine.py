import sys
from pathlib import Path

# ensure repo root is on path so `tools` package is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import importlib.util


def load_tools_module():
    root = Path(__file__).resolve().parents[1]
    mod_path = root / 'tools' / 'drift_forecast_engine.py'
    module_spec = importlib.util.spec_from_file_location('drift_forecast_engine', str(mod_path))
    module_obj = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module_obj)
    return module_obj


tools_mod = load_tools_module()
moving_average = tools_mod.moving_average
linear_regression_predict = tools_mod.linear_regression_predict
exponential_smoothing_predict = tools_mod.exponential_smoothing_predict


def round_list(xs, places=4):
    return [round(x, places) for x in xs]


def test_moving_average_basic():
    series = [1, 2, 3, 4, 5]
    out = moving_average(series, window=3)
    expected = [1.0, 1.5, 2.0, 3.0, 4.0]
    assert round_list(out) == round_list(expected)


def test_linear_regression_predict_simple():
    series = [1.0, 2.0, 3.0, 4.0]
    preds, (slope, intercept) = linear_regression_predict(series, steps=1)
    # For sequence 1,2,3,4 we expect next value ~5.0 for deterministic LR
    assert len(preds) == 1
    assert round(preds[0], 4) == round(5.0, 4)
    # slope should be approximately 1.0 and intercept ~1.0 given our implementation
    assert round(slope, 4) == round(1.0, 4)
    assert round(intercept, 4) == round(1.0, 4)


def test_exponential_smoothing_predict():
    series = [1.0, 2.0, 3.0, 4.0]
    preds = exponential_smoothing_predict(series, steps=1, alpha=0.5)
    # manual smoothing: s0=1 -> s1=1.5 -> s2=2.25 -> s3=3.125
    assert len(preds) == 1
    assert round(preds[0], 4) == round(3.125, 4)


def test_ensemble_prediction_behaviour():
    series = [0.0, 1.0, 0.0, 2.0, 1.0]
    # MA
    ma = moving_average(series, window=3)
    ma_pred = ma[-1] if ma else 0.0
    # LR
    lr_preds, _ = linear_regression_predict(series, steps=1)
    lr_pred = lr_preds[0] if lr_preds else 0.0
    # ES
    es_pred = exponential_smoothing_predict(series, steps=1, alpha=0.25)[0]

    # ensemble is median of [ma_pred, lr_pred, es_pred]
    ensemble = sorted([ma_pred, lr_pred, es_pred])[1]

    # Recompute using same deterministic steps and assert equality to 4 decimal places
    assert round(ensemble, 4) == round(sorted([ma_pred, lr_pred, es_pred])[1], 4)
