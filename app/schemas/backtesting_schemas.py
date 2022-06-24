from typing import Optional
from pydantic import BaseModel

class BacktestingMode(BaseModel):
    prodCode: str
    portfolioValue: int
    upperBound: Optional[int] = 0