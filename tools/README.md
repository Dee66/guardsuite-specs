GuardSuite Tools
=================

Purpose
-------
- Collection of deterministic analysis and forecasting utilities used by GuardSuite.
- Each tool is read-only with respect to product artifacts and produces deterministic outputs under the repository's conventions.

Tools Overview (deterministic alphabetical order)
------------------------------------------------
- `drift_alert_engine.py`: consumes `canonical_state/drift_history.json` and produces alerts (`drift_alerts.json`, `drift_alerts.md`) based on budgets and thresholds.
- `drift_engine.py`: compares canonical checksums and produces `drift_report.*` outputs (historical drift detection).
- `drift_forecast_engine.py`: forecasting engine that reads `canonical_state/drift_history.json` and writes `drift_forecast.json` and `drift_forecast.md` using MA, LR, and ES models.
- `drift_history_engine.py`: aggregates past snapshots into a temporal `drift_history.json`.
- `lineage_engine.py`: attributes drift to products/changes using deterministic heuristics and git history.
- `repair_runner.py` and `repair_rules/`: deterministic repair runner scaffolding for Strategy-E repairs.

Deterministic Constraints
-------------------------
- No network calls.
- No randomness or non-deterministic ordering: all collections are sorted (products ASC, files ASC) before processing.
- LF line endings for all generated files.
- Engines must not modify historical data; they only read canonical artifacts and write new outputs under `canonical_state/`.

Forecasting Models (formulas)
------------------------------
- Moving Average (MA, window w):

  MA_t = (1/w) * sum_{i=t-w+1..t} x_i

- Linear Regression (ordinary least squares): fit y = m*x + b on time indices x=0..n-1, predict at future t by m*t + b.

- Exponential Smoothing (ES, alpha α):

  s_0 = x_0
  s_t = α * x_t + (1-α) * s_{t-1}

  Predictions use the last smoothed value as the next-step forecast.

Usage Examples
--------------
Run the alert engine:
```bash
python3 tools/drift_alert_engine.py
```

Run the forecasting engine:
```bash
python3 tools/drift_forecast_engine.py
```

Run the lineage engine:
```bash
python3 tools/lineage_engine.py
```

Workflow (typical)
------------------
1. Validate rule specs and generate canonical snapshots.
2. Run `drift_engine.py` to detect drift.
3. Run `lineage_engine.py` to map drift to products.
4. Run `drift_history_engine.py` to aggregate temporal snapshots.
5. Run `drift_forecast_engine.py` to predict future drift and risk.
6. Run `drift_alert_engine.py` to surface alerts based on budgets and thresholds.

Contact
-------
For changes to these tools, open a PR against the repository's `main` branch and include deterministic test coverage.
