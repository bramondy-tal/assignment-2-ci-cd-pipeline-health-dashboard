from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LastStatusResponse(BaseModel):
    repo: str
    branch: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime]
    duration_seconds: Optional[float]
