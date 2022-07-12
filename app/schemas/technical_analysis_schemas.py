from typing import Optional
from pydantic import BaseModel

class GetDoneTradeModel(BaseModel):
    # fromTime: Search From Trade Time(YYYY-MM-DD HH:mm:ss)
    # toTime: Search To Trade Time(YYYY-MM-DD HH:mm:ss)
    sessionToken: str
    targetAccNo: str = 'ANSONLI01'
    fromTime: Optional[str] = None
    toTime: Optional[str] = None
    sortBy: Optional[str] = "prod_code, time_stamp"
    sort: Optional[str] = "ASC, ASC"

# class reportModel(GetDoneTradeModel):
#     pass