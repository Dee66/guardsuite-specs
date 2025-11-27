import os
from api.db import load_db, save_db

WEBHOOK_SECRET = os.environ.get("GUARDSUITE_WEBHOOK_SECRET", "")


def ingest_scan_result(payload, headers):
    secret = headers.get("X-Webhook-Secret")
    if secret != WEBHOOK_SECRET:
        return {"error": "invalid_secret"}

    pid = payload.get("product_id")
    task_id = payload.get("task_id")
    summary = payload.get("summary")
    contract = payload.get("feedback_contract")

    db = load_db()
    product = db.get(pid)
    if not product:
        return {"error": "product_not_found"}

    product.setdefault("audit_history", [])
    product["audit_history"].append(
        {
            "task_id": task_id,
            "summary": summary,
            "feedback_contract": contract,
        }
    )
    save_db(db)

    return {"status": "ok"}
