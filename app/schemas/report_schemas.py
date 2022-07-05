from typing import Optional
from pydantic import BaseModel

class reportModel(BaseModel):
    # fromTime: Search From Trade Time(YYYY-MM-DD HH:mm:ss)
    # toTime: Search To Trade Time(YYYY-MM-DD HH:mm:ss)
    sessionToken: str
    targetAccNo: str = 'ANSONLI01'