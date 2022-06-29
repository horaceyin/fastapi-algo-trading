from typing import Optional
from pydantic import BaseModel

class GetDoneTradeModel(BaseModel):
    sessionToken: str
    targetAccNo: str
    fromTime : Optional[str]
    toTime : Optional[str]