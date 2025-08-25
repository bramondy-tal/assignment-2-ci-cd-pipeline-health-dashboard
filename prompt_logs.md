# Prompt Logs

## Phase 1 – Backend Metrics APIs

### Requirement Definition
- **User**: Write a `requirements.md` file for metric APIs:
  - Success/Failure rate
  - Average build time
  - Last build status
  - Keep it simple, only basic requirements.

### Scaffolding Project
- **User**: Generate a project scaffold based on `requirements.md` and `design.md` with:
  - FastAPI backend with placeholder endpoints for:
    - `/metrics/success-rate`
    - `/metrics/average-duration`
    - `/metrics/last-status`
  - TimescaleDB migrations for `builds` table.
  - Docker Compose for FastAPI + TimescaleDB.
  - Basic folder structure (`app/routers`, `app/models`, `app/schemas`).

### Implementing Success Rate API
- **User**: Implement the `/metrics/success-rate` endpoint in FastAPI.
  - Use the `builds` table in TimescaleDB.
  - Support optional filters: `repo`, `branch`, `from`, `to`.
  - Return JSON with success rate, counts, and time window.

### Testing Success Rate
- **User**: Write `pytest` tests to validate `/metrics/success-rate` endpoint with different filter combinations.

### Implementing Average Duration API
- **User**: Implement the `/metrics/average-duration` endpoint in FastAPI.
  - Query `builds` table for duration.
  - Support optional filters: `repo`, `branch`, `from`, `to`.
  - Return JSON with average duration (seconds), build count, and time window.

### Implementing Last Build Status API
- **User**: Implement the `/metrics/last-status` endpoint in FastAPI.
  - Return latest build info (`repo`, `branch`, `status`, `started_at`, `finished_at`, `duration_seconds`).

---

## Phase 2 – Email Alerts

### Adding Alerts
- **User**: Implement email alerting for failed builds.
  - Requirements:
    - Use `FastAPI-Mail` (or similar) with SMTP.
    - When ingesting a new build with `status="failure"`, send email.
    - Email should include `repo`, `branch`, `status`, `duration`, link to GitHub run.
    - Config via environment variables (SMTP host, port, username, password, recipients).
    - Deduplicate alerts using `github_run_id`.

---

## Phase 3 – UI Visualization

### Dashboard Integration
- **User**: Build a React + Tailwind UI dashboard to visualize backend metrics.
  - Requirements:
    - Start with repository ingestion (form to input `repo` + `branch`).
    - After ingestion, show metrics:
      - Success/Failure rate.
      - Average build time.
      - Last status.
    - Add table of latest builds with `status` + `duration` + GitHub run link.
    - Optional filters: date range, auto-refresh.
    - Clean, minimalistic design.

---

## Debugging and Issue Resolution

### Debugging API Issues
- **User**: Encountered CORS errors when the frontend tried to access the backend.
- **AI**: Enabled CORS middleware in FastAPI to resolve the issue.

### Fixing Frontend Accessibility
- **User**: Frontend was not accessible on `http://localhost:5173`.
- **AI**: Updated `vite.config.js` to bind the server to `0.0.0.0` and explicitly set the port to `5173`.

### Resolving Docker Configuration Errors
- **User**: Faced `ContainerConfig` errors during Docker Compose setup.
- **AI**: Cleaned up Docker resources and fixed volume declarations in `docker-compose.yml`.

### Database Migration Issues
- **User**: Migrations were not applied due to incorrect container name.
- **AI**: Corrected the database container name in the migration commands and ensured the migrations were applied successfully.

### Setting Up Tests
- **User**: Faced issues while setting up the `tests/` directory for the backend.
- **AI**: Provided guidance on structuring `pytest` tests and configuring `conftest.py` for database fixtures.

### Implementing Metrics with the Database
- **User**: Encountered challenges while querying the `builds` table for metrics APIs.
- **AI**: Assisted in writing optimized SQL queries for:
  - Success/Failure rate.
  - Average build duration.
  - Last build status.
- **AI**: Debugged issues with SQLAlchemy models and ensured proper integration with TimescaleDB.

### Testing and Validation
- **User**: Tested the application end-to-end after resolving all issues.
- **AI**: Verified the functionality of metrics APIs, email alerts, and the dashboard UI.