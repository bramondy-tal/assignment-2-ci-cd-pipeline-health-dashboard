import os
from sqlalchemy import text
from app.email_utils import send_failure_email

RECIPIENTS = os.getenv("SMTP_RECIPIENTS", "").split(",")

async def maybe_send_failure_alert(db, build):
    # Deduplicate: check if alert already sent
    sql = text("SELECT 1 FROM build_alerts WHERE github_run_id = :run_id LIMIT 1")
    res = await db.execute(sql, {"run_id": build["github_run_id"]})
    if res.fetchone():
        return  # Already alerted
    if build["status"] != "failure":
        return
    await send_failure_email(
        repo=build["repo"],
        branch=build["branch"],
        status=build["status"],
        duration=build["duration_seconds"],
        github_run_id=build["github_run_id"],
        recipients=[r.strip() for r in RECIPIENTS if r.strip()]
    )
    # Mark as alerted
    await db.execute(
        text("INSERT INTO build_alerts (github_run_id, sent_at) VALUES (:run_id, CURRENT_TIMESTAMP)"),
        {"run_id": build["github_run_id"]}
    )
    await db.commit()
