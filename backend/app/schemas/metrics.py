from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SuccessRateResponse(BaseModel):
    success_rate: float
    success_count: int
    failure_count: int
    total: int
    from_: Optional[datetime]
    to: Optional[datetime]
