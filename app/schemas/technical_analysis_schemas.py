from typing import Optional
from pydantic import BaseModel
from typing import Optional

class GetDoneTradeModel(BaseModel):
    # fromTime: Search From Trade Time(YYYY-MM-DD HH:mm:ss)
    # toTime: Search To Trade Time(YYYY-MM-DD HH:mm:ss)
    sessionToken: str
    targetAccNo: str
    fromTime: Optional[str] = None
    toTime: Optional[str] = None
    
