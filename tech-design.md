# CI/CD Pipeline Health Dashboard - Design

## 1. API Endpoints

### 1.1. Success/Failure Rate
- **Endpoint:** `GET /metrics/success-rate`
- **Query Params:**
  - `repo` (string, optional)
  - `branch` (string, optional)
  - `from` (ISO datetime, optional)
  - `to` (ISO datetime, optional)
- **Response:**
```json
{
  "success_rate": 0.92,
  "success_count": 23,
  "failure_count": 2,
  "total": 25,
  "from": "2025-08-20T00:00:00Z",
  "to": "2025-08-22T00:00:00Z"
}
```

### 1.2. Average Build Duration
- **Endpoint:** `GET /metrics/average-duration`
- **Query Params:**
  - `repo` (string, optional)
  - `branch` (string, optional)
  - `from` (ISO datetime, optional)
  - `to` (ISO datetime, optional)
- **Response:**
```json
{
  "average_duration_seconds": 120.5,
  "build_count": 25,
  "from": "2025-08-20T00:00:00Z",
  "to": "2025-08-22T00:00:00Z"
}
```

### 1.3. Last Build Status
- **Endpoint:** `GET /metrics/last-status`
- **Query Params:**
  - `repo` (string, optional)
  - `branch` (string, optional)
- **Response:**
```json
{
  "repo": "myorg/myrepo",
  "branch": "main",
  "status": "success", // or "failure", "in_progress"
  "started_at": "2025-08-22T10:00:00Z",
  "finished_at": "2025-08-22T10:02:00Z",
  "duration_seconds": 120
}
```

---

## 2. Database Schema (TimescaleDB)

### 2.1. Table: builds
```sql
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    github_run_id BIGINT NOT NULL,
    repo VARCHAR(255) NOT NULL,
    branch VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL, -- success, failure, in_progress
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    duration_seconds FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable for TimescaleDB
do $$
begin
  IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'builds') THEN
    SELECT create_hypertable('builds', 'started_at', if_not_exists => TRUE);
  END IF;
end$$;
```

### 2.2. Table: logs (optional, for build logs or error messages)
```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    build_id INTEGER REFERENCES builds(id),
    log_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 3. High-Level Architecture

1. **Ingestion**
    - Scheduled job (e.g., APScheduler) fetches workflow runs from GitHub Actions REST API.
    - Extracts relevant metadata (repo, branch, status, timestamps, duration).
    - Stores data in TimescaleDB `builds` table.

2. **Metrics Computation**
    - FastAPI endpoints query TimescaleDB for metrics (success rate, average duration, last status) using SQL aggregations and time filters.
    - Endpoints support filtering by repo, branch, and time range.

3. **Alerting**
    - On ingesting a failed build, FastAPI triggers an email notification (via FastAPI-Mail) to configured recipients.
    - Email includes repo, branch, build status, and a link to the GitHub Actions run.

4. **Frontend**
    - React/Next.js dashboard fetches metrics from FastAPI endpoints and visualizes them.

5. **Containerization**
    - All components (FastAPI, TimescaleDB, Next.js) run in Docker containers, orchestrated by docker-compose.
