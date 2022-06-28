from typing import Optional
from pydantic import BaseModel

import json

class BacktestingModel(BaseModel):
    prodCode: str
    portfolioValue: Optional[int] = 0 # avFund # Default value should be the user's portfolio size
    upperBound: Optional[int] = 0
    userid: Optional[str]
    password: Optional[str]
    targetAcc: Optional[str] = "SPTEST"