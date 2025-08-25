import os
import httpx
from typing import List, Dict, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.email_alerts import maybe_send_failure_alert

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

async def fetch_github_workflow_runs(owner: str, repo: str, session: AsyncSession, branch: str = None, per_page: int = 40):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    params = {"per_page": per_page}
    if branch:
        params["branch"] = branch
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/runs"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        runs = data.get("workflow_runs", [])
        for run in runs:
            await upsert_build_from_run(run, session)

async def upsert_build_from_run(run: Dict[str, Any], session: AsyncSession):
    sql = text('''
        INSERT INTO builds (github_run_id, started_at, repo, branch, status, finished_at, duration_seconds)
        VALUES (:github_run_id, :started_at, :repo, :branch, :status, :finished_at, :duration_seconds)
        ON CONFLICT (github_run_id, started_at) DO UPDATE SET
            status = EXCLUDED.status,
            finished_at = EXCLUDED.finished_at,
            duration_seconds = EXCLUDED.duration_seconds
    ''')
    started_at_raw = run.get("run_started_at") or run.get("created_at")
    finished_at_raw = run.get("updated_at")
    dt_start = None
    dt_end = None
    duration = None
    try:
        if started_at_raw:
            dt_start = datetime.fromisoformat(started_at_raw.replace("Z", "+00:00"))
        if finished_at_raw:
            dt_end = datetime.fromisoformat(finished_at_raw.replace("Z", "+00:00"))
        if dt_start and dt_end:
            duration = (dt_end - dt_start).total_seconds()
    except Exception:
        duration = None
    build = {
        "github_run_id": run["id"],
        "started_at": dt_start,
        "repo": run["repository"].get("full_name") if run.get("repository") else run.get("repository_full_name", "unknown/unknown"),
        "branch": run.get("head_branch", "unknown"),
        "status": run.get("conclusion") or run.get("status"),
        "finished_at": dt_end,
        "duration_seconds": duration
    }
    await session.execute(sql, build)
    await session.commit()
    # Email notifications for failed workflows are now handled only via webhook, not ingestion.
