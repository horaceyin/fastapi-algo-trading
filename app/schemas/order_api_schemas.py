from typing import Optional, Literal
from pydantic import BaseModel

class AddOrder(BaseModel):
    accNo: str
    buySell: Literal["B", "S"] # B or S
    condType: Literal[0, 1, 3, 4, 6, 8, 9] # 0, 1 (Stop), 3, 4, 6, 8, 9
    orderType: Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
    priceInDec: float
    prodCode: str
    qty: int
    sessionToken: str
    validType: Literal[0, 1, 2, 3, 4] = 0 # 0 - 4
    clOrderId: Optional[str] 
    # downLevelInDec: Optional[float]
    # downPriceInDec: Optional[float]
    openClose: Optional[Literal["M", "O", "C"]] # M, O, C
    # options: Optional[int] # Unsure of purpose
    # ref: Optional[str]
    # ref2: Optional[str]
    schedTime: Optional[float] # In the form YYYYMMDD.hhmmss
    status: Optional[int] # Only reauired in inactive orders (2 = Inactive)
    stopPriceInDec: Optional[int]
    stopType: Optional[Literal["L", "U", "D"]] # L, U, D, or blank
    subCondType: Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0, 1 (Stop), 3, 4, 6, 11, 14, 16 
    # upLevelInDec: Optional[float]
    # upPriceInDec: Optional[float]
    # validDate: Optional[int] # YYYYMMDD

class ChangeOrder(BaseModel):
    accNo: str
    accOrderNo: int
    buySell: Literal["B", "S"]
    prodCode: str
    sessionToken: str
    # downLevelInDec: Optional[float]
    # downPriceInDec: Optional[float]
    extOrderId: str
    priceInDec: Optional[float]
    qty: Optional[int]
    schedTime: Optional[float] # In the form YYYYMMDD.hhmmss
    stopPriceInDec: Optional[int]
    # upLevelInDec: Optional[float]
    # upPriceInDec: Optional[float]
    # validDate: Optional[int] # YYYYMMDD

class DeleteOrder(BaseModel):
    accNo: str
    accOrderNo: int
    buySell: Literal["B", "S"]
    prodCode: str
    sessionToken: str
    extOrderId: str