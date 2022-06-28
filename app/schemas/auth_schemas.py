from typing import Optional
from pydantic import BaseModel

class UserLogin(BaseModel):
    apiAppId: Optional[str] = "SP_F"
    mode: Optional[int] = 0
    password: str
    userId: str

class UserInfo(BaseModel):
    sessionToken:str
    targetAccNo: str
    dataSource: Optional[int] = 4