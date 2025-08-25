import os
import pytest
import pytest_asyncio
from sqlalchemy import text
from backend.app.models.email_alerts import maybe_send_failure_alert

@pytest_asyncio.fixture(autouse=True)
async def setup_alerts_table(db_session):
    await db_session.execute(text("DELETE FROM build_alerts"))
    await db_session.commit()
    yield

@pytest.mark.asyncio
async def test_email_sent_once(monkeypatch, db_session):
    sent = []
    async def fake_send_failure_email(**kwargs):
        sent.append(kwargs)
    monkeypatch.setattr("backend.app.models.email_alerts.send_failure_email", fake_send_failure_email)
    build = {
        "github_run_id": 123,
        "repo": "myorg/myrepo",
        "branch": "main",
        "status": "failure",
        "duration_seconds": 42,
    }
    await maybe_send_failure_alert(db_session, build)
    await maybe_send_failure_alert(db_session, build)  # Should not send again
    assert len(sent) == 1
    assert sent[0]["repo"] == "myorg/myrepo"
    assert sent[0]["branch"] == "main"
    assert sent[0]["status"] == "failure"
    assert sent[0]["duration"] == 42
    assert "github_run_id" in sent[0]

@pytest.mark.asyncio
async def test_no_email_on_success(monkeypatch, db_session):
    sent = []
    async def fake_send_failure_email(**kwargs):
        sent.append(kwargs)
    monkeypatch.setattr("backend.app.models.email_alerts.send_failure_email", fake_send_failure_email)
    build = {
        "github_run_id": 456,
        "repo": "myorg/myrepo",
        "branch": "main",
        "status": "success",
        "duration_seconds": 99,
    }
    await maybe_send_failure_alert(db_session, build)
    assert not sent
