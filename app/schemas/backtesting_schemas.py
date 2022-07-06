from typing import Optional
from pydantic import BaseModel

import json

class BacktestingModel(BaseModel):
    prodCode: str = "YMU2" # 6EN2
    portfolioValue: int = 10000000 # avFund # Default value should be the user's portfolio size
    barSummary: int = 5 # Bar summarizes the trading activity during barSummary seconds
    boundaryValue: int = 0
    userid: Optional[str]
    password: Optional[str]
    targetAcc: Optional[str] = "SPTEST"