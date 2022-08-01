from typing import Optional
from pydantic import BaseModel

class UserLogin(BaseModel):
    apiAppId: Optional[str] = 'SP_F'
    mode: Optional[int] = 0
    password: str = 'sp'
    userId: str = 'NICHOLAS01' #ANSONLI01

class AccountSumModel(BaseModel):
    sessionToken: str
    targetAccNo: str = 'NICHOLAS01'
    dataSource: Optional[int] = 4
    password: str = 'sp'

class AccountOrder(BaseModel):
    sessionToken: str
    targetAccNo: str
    dataSource: Optional[int] = 4
    userId: str = 'NICHOLAS01'
