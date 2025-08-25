

from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import metrics
from app.models.db import get_db
from app.models.github_ingest import fetch_github_workflow_runs
from app.models.email_alerts import maybe_send_failure_alert
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

# Test endpoint to trigger ingestion manually
@app.post("/ingest/github-actions")
async def ingest_github_actions(owner: str, repo: str, branch: str = None, db: AsyncSession = Depends(get_db)):
	await fetch_github_workflow_runs(owner, repo, db, branch=branch)
	return {"status": "ingestion complete"}


# Webhook endpoint for GitHub Actions workflow run events
@app.post("/webhook/github-actions")
async def github_actions_webhook(request: Request, db: AsyncSession = Depends(get_db)):
	payload = await request.json()
	action = payload.get("action")
	workflow_run = payload.get("workflow_run")
	if action == "completed" and workflow_run:
		status_ = workflow_run.get("conclusion")
		if status_ == "failure":
			build = {
				"github_run_id": workflow_run["id"],
				"started_at": workflow_run.get("run_started_at") or workflow_run.get("created_at"),
				"repo": workflow_run.get("repository", {}).get("full_name", "unknown/unknown"),
				"branch": workflow_run.get("head_branch", "unknown"),
				"status": status_,
				"finished_at": workflow_run.get("updated_at"),
				"duration_seconds": None  # Optional: calculate if needed
			}
			await maybe_send_failure_alert(db, build)
	return JSONResponse(content={"ok": True}, status_code=status.HTTP_200_OK)
