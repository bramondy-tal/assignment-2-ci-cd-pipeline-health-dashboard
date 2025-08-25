
from fastapi import APIRouter, Query, Depends, HTTPException
from datetime import datetime
from typing import Optional
from sqlalchemy import text
from app.models.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.metrics import SuccessRateResponse
from app.schemas.average_duration import AverageDurationResponse
from app.schemas.last_status import LastStatusResponse

router = APIRouter()

@router.get("/success-rate", response_model=SuccessRateResponse)
async def get_success_rate(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    from_: Optional[datetime] = Query(None, alias="from"),
    to: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    filters = []
    params = {}
    if repo:
        filters.append("repo = :repo")
        params["repo"] = repo
    if branch:
        filters.append("branch = :branch")
        params["branch"] = branch
    if from_:
        filters.append("started_at >= :from_")
        params["from_"] = from_
    if to:
        # If 'to' is a date (no time), set to end of day
        if isinstance(to, datetime) and to.hour == 0 and to.minute == 0 and to.second == 0 and to.microsecond == 0:
            to = to.replace(hour=23, minute=59, second=59, microsecond=999999)
        filters.append("started_at <= :to")
        params["to"] = to
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    sql = f'''
        SELECT
            COUNT(*) FILTER (WHERE status = 'success') AS success_count,
            COUNT(*) FILTER (WHERE status = 'failure') AS failure_count,
            COUNT(*) AS total
        FROM builds
        {where_clause}
    '''
    result = await db.execute(text(sql), params)
    row = result.fetchone()
    if not row or row.total == 0:
        return SuccessRateResponse(
            success_rate=0.0,
            success_count=0,
            failure_count=0,
            total=0,
            from_=from_,
            to=to
        )
    success_rate = row.success_count / row.total if row.total else 0.0
    return SuccessRateResponse(
        success_rate=success_rate,
        success_count=row.success_count,
        failure_count=row.failure_count,
        total=row.total,
        from_=from_,
        to=to
    )


@router.get("/average-duration", response_model=AverageDurationResponse)
async def get_average_duration(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    from_: Optional[datetime] = Query(None, alias="from"),
    to: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    filters = []
    params = {}
    if repo:
        filters.append("repo = :repo")
        params["repo"] = repo
    if branch:
        filters.append("branch = :branch")
        params["branch"] = branch
    if from_:
        filters.append("started_at >= :from_")
        params["from_"] = from_
    if to:
        if isinstance(to, datetime) and to.hour == 0 and to.minute == 0 and to.second == 0 and to.microsecond == 0:
            to = to.replace(hour=23, minute=59, second=59, microsecond=999999)
        filters.append("started_at <= :to")
        params["to"] = to
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    sql = f'''
        SELECT
            AVG(duration_seconds) AS average_duration_seconds,
            COUNT(*) AS build_count
        FROM builds
        {where_clause}
    '''
    result = await db.execute(text(sql), params)
    row = result.fetchone()
    avg_duration = row.average_duration_seconds if row and row.average_duration_seconds is not None else 0.0
    build_count = row.build_count if row and row.build_count is not None else 0
    return AverageDurationResponse(
        average_duration_seconds=avg_duration,
        build_count=build_count,
        from_=from_,
        to=to
    )


@router.get("/last-status", response_model=LastStatusResponse)
async def get_last_status(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    filters = []
    params = {}
    if repo:
        filters.append("repo = :repo")
        params["repo"] = repo
    if branch:
        filters.append("branch = :branch")
        params["branch"] = branch
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    sql = f'''
        SELECT repo, branch, status, started_at, finished_at, duration_seconds
        FROM builds
        {where_clause}
        ORDER BY started_at DESC
        LIMIT 1
    '''
    result = await db.execute(text(sql), params)
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No builds found for the given filters.")
    return LastStatusResponse(
        repo=row.repo,
        branch=row.branch,
        status=row.status,
        started_at=row.started_at,
        finished_at=row.finished_at,
        duration_seconds=row.duration_seconds
    )
