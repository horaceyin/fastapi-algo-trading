from typing import Optional
from pydantic import BaseModel

class ReportModel(BaseModel):
    # fromTime: Search From Trade Time(YYYY-MM-DD HH:mm:ss)
    # toTime: Search To Trade Time(YYYY-MM-DD HH:mm:ss)
    sessionToken: str
    targetAccNo: str = 'NICHOLAS01' # ANSONLI01