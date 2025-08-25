from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AverageDurationResponse(BaseModel):
    average_duration_seconds: float
    build_count: int
    from_: Optional[datetime]
    to: Optional[datetime]
