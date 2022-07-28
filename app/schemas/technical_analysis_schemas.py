from typing import Optional
from pydantic import BaseModel
class GetDoneTradeModel(BaseModel):
    # fromTime: Search From Trade Time(YYYY-MM-DD HH:mm:ss)
    # toTime: Search To Trade Time(YYYY-MM-DD HH:mm:ss)
    systemId: str = 'SP_F'
    ssoToken: str
    ssoTime: str
    userId: str = 'NICHOLAS01' # or ANSONLI01
    targetAccNo: str = 'NICHOLAS01' # or ANSONLI01
    fromTime: Optional[str] = None
    toTime: Optional[str] = None
    sortBy: Optional[str] = "prod_code,time_stamp"
    sort: Optional[str] = "ASC,ASC"

class GetContractSize(BaseModel):
    sessionToken: str
    dataRecordTotal: int = 100
    dataStartFromRecord: int = 0
    instmntCode: str 
    underlying: Optional[str]
# class reportModel(GetDoneTradeModel):
#     pass