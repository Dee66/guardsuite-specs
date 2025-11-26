#!/usr/bin/env python3
"""
Deterministic drift forecasting engine.

Reads `canonical_state/drift_history.json` and produces forecasts using
3-period moving average, simple linear regression, and exponential
smoothing (alpha=0.25). Writes `canonical_state/drift_forecast.json` and
`canonical_state/drift_forecast.md`.

All outputs are deterministic and sorted (products ASC, files ASC).
No network calls. No modifications to historical data.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import sys


MA_WINDOW = 3
ALPHA = 0.25
DEFAULT_DRIFT_BUDGET = 5


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def moving_average(series, window=MA_WINDOW):
    if not series:
        return []
    out = []
    for i in range(len(series)):
        start = max(0, i - window + 1)
        window_vals = series[start:i+1]
        out.append(sum(window_vals)/len(window_vals))
    return out


def linear_regression_predict(series, steps=1):
    # deterministic least squares linear regression on (t, y)
    n = len(series)
    if n == 0:
        return [0]*steps, (0.0, 0.0)  # preds, (slope, intercept)
    xs = list(range(n))
    ys = series
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xx = sum(x*x for x in xs)
    sum_xy = sum(x*y for x,y in zip(xs, ys))
    denom = n * sum_xx - sum_x * sum_x
    if denom == 0:
        slope = 0.0
    else:
        slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    preds = []
    for s in range(1, steps+1):
        t = n - 1 + s
        preds.append(slope * t + intercept)
    return preds, (slope, intercept)


def exponential_smoothing_predict(series, steps=1, alpha=ALPHA):
    if not series:
        return [0]*steps
    s = series[0]
    for val in series[1:]:
        s = alpha * val + (1 - alpha) * s
    # naive: continue smoothing using last smoothed value
    preds = []
    last = s
    for _ in range(steps):
        preds.append(last)
    return preds


def aggregate_event_counts(history):
    # history expected to have 'timepoints' and 'per_product' and 'per_file'
    timepoints = history.get('timepoints', [])
    # use ordered unique timestamps
    timestamps = [tp.get('timestamp') for tp in timepoints if tp.get('timestamp')]
    timestamps = sorted(list(dict.fromkeys(timestamps)))

    per_product = {}
    raw_per_product = history.get('per_product', {})
    for prod in sorted(raw_per_product.keys()):
        # build series aligned to timestamps
        series = []
        timeline = raw_per_product[prod].get('timeline', [])
        # map ts->count
        m = {e.get('timestamp'): (e.get('changed',0) + e.get('added',0) + e.get('removed',0)) for e in timeline if e.get('timestamp')}
        for ts in timestamps:
            series.append(int(m.get(ts, 0)))
        per_product[prod] = {'timestamps': timestamps, 'series': series}

    per_file = {}
    raw_per_file = history.get('per_file', {})
    for fp in sorted(raw_per_file.keys()):
        timeline = raw_per_file[fp].get('timeline', [])
        m = {e.get('timestamp'): (1 if e.get('state') in ('changed','added','removed') else 0) for e in timeline if e.get('timestamp')}
        series = [int(m.get(ts, 0)) for ts in timestamps]
        per_file[fp] = {'timestamps': timestamps, 'series': series}

    return timestamps, per_product, per_file


def compute_forecasts(history):
    timestamps, per_product, per_file = aggregate_event_counts(history)
    results = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'ma_window': MA_WINDOW,
        'alpha': ALPHA,
        'products': {},
        'files': {},
    }

    for prod in sorted(per_product.keys()):
        series = per_product[prod]['series']
        # moving average (take last MA_WINDOW value as prediction for next)
        ma_series = moving_average(series, MA_WINDOW)
        ma_pred_1 = ma_series[-1] if ma_series else 0.0
        # for horizon, use trailing average
        ma_pred_3 = ma_pred_1
        ma_pred_10 = ma_pred_1

        # linear regression
        lr_preds_1, (slope, intercept) = linear_regression_predict(series, steps=1)
        lr_preds_3, _ = linear_regression_predict(series, steps=3)
        lr_preds_10, _ = linear_regression_predict(series, steps=10)

        # exponential smoothing
        es_pred_1 = exponential_smoothing_predict(series, steps=1, alpha=ALPHA)[0]
        es_pred_3 = es_pred_1
        es_pred_10 = es_pred_1

        # ensemble: median of the three method predictions for each horizon (deterministic order)
        def ensemble(preds):
            sorted_preds = sorted(preds)
            m = sorted_preds[len(sorted_preds)//2]
            return max(0.0, m)

        p1 = ensemble([ma_pred_1, lr_preds_1[0] if lr_preds_1 else 0.0, es_pred_1])
        p3 = ensemble([ma_pred_3, (lr_preds_3[-1] if lr_preds_3 else 0.0), es_pred_3])
        p10 = ensemble([ma_pred_10, (lr_preds_10[-1] if lr_preds_10 else 0.0), es_pred_10])

        budget = history.get('budgets', {}).get('per_product', DEFAULT_DRIFT_BUDGET)
        if budget is None:
            budget = DEFAULT_DRIFT_BUDGET
        risk = min(100.0, (p1 / float(budget)) * 100.0 if budget > 0 else 100.0)

        results['products'][prod] = {
            'series': series,
            'predictions': {
                'ma': {'1': round(ma_pred_1, 3), '3': round(ma_pred_3, 3), '10': round(ma_pred_10, 3)},
                'lr': {'1': round(lr_preds_1[0], 3) if lr_preds_1 else 0.0, '3': round(lr_preds_3[-1],3) if lr_preds_3 else 0.0, '10': round(lr_preds_10[-1],3) if lr_preds_10 else 0.0},
                'es': {'1': round(es_pred_1, 3), '3': round(es_pred_3, 3), '10': round(es_pred_10, 3)},
                'ensemble': {'1': round(p1,3), '3': round(p3,3), '10': round(p10,3)},
            },
            'risk_score': round(risk, 2),
            'model_params': {'lr_slope': round(slope,6), 'lr_intercept': round(intercept,6)},
            'budget': budget,
        }

    # per-file next-step predictions (1 step ahead) using ensemble of LR and ES and MA
    for fp in sorted(per_file.keys()):
        series = per_file[fp]['series']
        ma_series = moving_average(series, MA_WINDOW)
        ma_pred = ma_series[-1] if ma_series else 0.0
        lr_preds, (slope, intercept) = linear_regression_predict(series, steps=1)
        es_pred = exponential_smoothing_predict(series, steps=1, alpha=ALPHA)[0]
        p1 = sorted([ma_pred, lr_preds[0] if lr_preds else 0.0, es_pred])[1]
        results['files'][fp] = {'series': series, 'prediction_1': round(max(0.0, p1),3), 'model_params': {'lr_slope': round(slope,6), 'lr_intercept': round(intercept,6)}}

    return results


def write_reports(out_json: Path, out_md: Path, report):
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)

    # Markdown summary
    lines = []
    lines.append('# GuardSuite Drift Forecast')
    lines.append(f"**Generated:** {report.get('generated')}")
    lines.append('')
    lines.append('## Products Risk Summary')
    # products sorted
    for prod in sorted(report['products'].keys()):
        p = report['products'][prod]
        lines.append(f"- {prod}: next-step ensemble={p['predictions']['ensemble']['1']} risk={p['risk_score']}% (budget {p['budget']})")
    lines.append('')
    lines.append('## Files Next-Step Predictions (1)')
    for fp in sorted(report['files'].keys()):
        f = report['files'][fp]
        lines.append(f"- {fp}: predicted={f['prediction_1']}")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    with out_md.open('w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')


def main(argv):
    root = Path('canonical_state')
    hist = root / 'drift_history.json'
    if not hist.exists():
        print('canonical_state/drift_history.json not found', file=sys.stderr)
        return 2
    history = load_json(hist)
    report = compute_forecasts(history)
    out_json = root / 'drift_forecast.json'
    out_md = root / 'drift_forecast.md'
    write_reports(out_json, out_md, report)
    print('WROTE', out_json, 'and', out_md)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
