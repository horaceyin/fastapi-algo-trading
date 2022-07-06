from typing import Optional
from pydantic import BaseModel

import json

class BacktestingModel(BaseModel):
    prodCode: str
    portfolioValue: int = 0 # avFund # Default value should be the user's portfolio size
    barSummary: int = 1 # Bar summarizes the trading activity during barSummary seconds
    boundaryValue: int = 0
    userid: Optional[str]
    password: Optional[str]
    targetAcc: Optional[str] = "SPTEST"