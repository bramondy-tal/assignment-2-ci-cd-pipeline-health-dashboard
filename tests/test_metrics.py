import pytest
from datetime import datetime, timedelta
from sqlalchemy import text

import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from sqlalchemy import text

async def seed_builds(db_session):
    now = datetime.utcnow()
    builds = [
        # repo1/main: 2 success, 1 failure
        {
            "github_run_id": 1,
            "started_at": now - timedelta(days=3),
            "repo": "repo1",
            "branch": "main",
            "status": "success",
            "finished_at": now - timedelta(days=3, minutes=-2),
            "duration_seconds": 120,
        },
        {
            "github_run_id": 2,
            "started_at": now - timedelta(days=2),
            "repo": "repo1",
            "branch": "main",
            "status": "failure",
            "finished_at": now - timedelta(days=2, minutes=-3),
            "duration_seconds": 180,
        },
        {
            "github_run_id": 3,
            "started_at": now - timedelta(days=1),
            "repo": "repo1",
            "branch": "main",
            "status": "success",
            "finished_at": now - timedelta(days=1, minutes=-1),
            "duration_seconds": 60,
        },
        # repo1/dev: 1 success
        {
            "github_run_id": 4,
            "started_at": now - timedelta(days=1, hours=1),
            "repo": "repo1",
            "branch": "dev",
            "status": "success",
            "finished_at": now - timedelta(days=1, hours=1, minutes=-4),
            "duration_seconds": 240,
        },
        # repo2/main: 1 failure
        {
            "github_run_id": 5,
            "started_at": now - timedelta(days=4),
            "repo": "repo2",
            "branch": "main",
            "status": "failure",
            "finished_at": now - timedelta(days=4, minutes=-5),
            "duration_seconds": 300,
        },
    ]
    await db_session.execute(
        text("""
            INSERT INTO builds (github_run_id, started_at, repo, branch, status, finished_at, duration_seconds)
            VALUES (:github_run_id, :started_at, :repo, :branch, :status, :finished_at, :duration_seconds)
        """),
        builds,
    )
    await db_session.commit()


@pytest_asyncio.fixture(autouse=True)
async def setup_data(db_session):
    await db_session.execute(text("DELETE FROM builds"))
    await seed_builds(db_session)
    yield


@pytest.mark.asyncio
async def test_success_rate_basic(client):
    resp = await client.get("/metrics/success-rate")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success_count"] == 3
    assert data["failure_count"] == 2
    assert data["total"] == 5
    assert abs(data["success_rate"] - 0.6) < 0.01


@pytest.mark.asyncio
async def test_success_rate_filters(client):
    resp = await client.get("/metrics/success-rate?repo=repo1&branch=main")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success_count"] == 2
    assert data["failure_count"] == 1
    assert data["total"] == 3
    assert abs(data["success_rate"] - 2/3) < 0.01


@pytest.mark.asyncio
async def test_success_rate_no_builds(client, db_session):
    await db_session.execute(text("DELETE FROM builds"))
    await db_session.commit()
    resp = await client.get("/metrics/success-rate?repo=none")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["success_rate"] == 0.0


@pytest.mark.asyncio
async def test_average_duration_basic(client):
    resp = await client.get("/metrics/average-duration")
    assert resp.status_code == 200
    data = resp.json()
    assert data["build_count"] == 5
    expected_avg = (120 + 180 + 60 + 240 + 300) / 5
    assert abs(data["average_duration_seconds"] - expected_avg) < 0.01


@pytest.mark.asyncio
async def test_average_duration_filters(client):
    resp = await client.get("/metrics/average-duration?repo=repo1&branch=main")
    assert resp.status_code == 200
    data = resp.json()
    assert data["build_count"] == 3
    expected_avg = (120 + 180 + 60) / 3
    assert abs(data["average_duration_seconds"] - expected_avg) < 0.01


@pytest.mark.asyncio
async def test_average_duration_no_builds(client, db_session):
    await db_session.execute(text("DELETE FROM builds"))
    await db_session.commit()
    resp = await client.get("/metrics/average-duration?repo=none")
    assert resp.status_code == 200
    data = resp.json()
    assert data["build_count"] == 0
    assert data["average_duration_seconds"] == 0.0


@pytest.mark.asyncio
async def test_last_status_basic(client):
    resp = await client.get("/metrics/last-status?repo=repo1&branch=main")
    assert resp.status_code == 200
    data = resp.json()
    assert data["repo"] == "repo1"
    assert data["branch"] == "main"
    assert data["status"] in ("success", "failure")


@pytest.mark.asyncio
async def test_last_status_no_builds(client, db_session):
    await db_session.execute(text("DELETE FROM builds"))
    await db_session.commit()
    resp = await client.get("/metrics/last-status?repo=none")
    assert resp.status_code == 404
