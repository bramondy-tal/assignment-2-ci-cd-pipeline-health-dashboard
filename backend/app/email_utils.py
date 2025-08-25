import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME="CI/CD Notifier",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_failure_email(repo: str, branch: str, status: str, duration: float, github_run_id: int, recipients: List[str]):
    url = f"https://github.com/{repo}/actions/runs/{github_run_id}"
    subject = f"[CI/CD] Build Failed: {repo} [{branch}]"
    body = f"""
    Repository: {repo}\n
    Branch: {branch}\n
    Status: {status}\n
    Duration: {duration} seconds\n
    GitHub Actions Run: {url}\n
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
