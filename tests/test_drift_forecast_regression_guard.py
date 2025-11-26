import json
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
compute_forecasts = tools_mod.compute_forecasts


def test_regression_guard_matches_forecast_file():
    root = Path('canonical_state')
    forecast_path = root / 'drift_forecast.json'
    history_path = root / 'drift_history.json'
    assert forecast_path.exists(), 'drift_forecast.json missing'
    assert history_path.exists(), 'drift_history.json missing'

    with forecast_path.open('r', encoding='utf-8') as f:
        stored = json.load(f)

    with history_path.open('r', encoding='utf-8') as f:
        history = json.load(f)

    regenerated = compute_forecasts(history)

    stored_products = stored.get('products', {})
    regen_products = regenerated.get('products', {})

    # Deterministic ordering: sort keys
    for prod in sorted(set(list(stored_products.keys()) + list(regen_products.keys()))):
        assert prod in regen_products, f'{prod} missing in regenerated'
        assert prod in stored_products, f'{prod} missing in stored forecast'
        s_pred = float(stored_products[prod]['predictions']['ensemble']['1'])
        r_pred = float(regen_products[prod]['predictions']['ensemble']['1'])
        s_risk = float(stored_products[prod].get('risk_score', 0.0))
        r_risk = float(regen_products[prod].get('risk_score', 0.0))

        # numeric equality with tolerance 1e-9
        assert abs(s_pred - r_pred) <= 1e-9, f'prediction mismatch for {prod}: {s_pred} != {r_pred}'
        assert abs(s_risk - r_risk) <= 1e-9, f'risk mismatch for {prod}: {s_risk} != {r_risk}'
