from typing import Optional, Literal, Dict
from pydantic import BaseModel, validator, root_validator

class AddOrder(BaseModel):
    accNo: str
    buySell: Literal["B", "S"] # B, S
    condType: Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9
    orderType: Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
    priceInDec: float
    prodCode: str
    qty: int
    sessionToken: str
    # sessionToken: Optional[str] # Set so it will be filled by system
    validType: Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
    clOrderId: Optional[str] 
    # downLevelInDec: Optional[float]
    # downPriceInDec: Optional[float]
    openClose: Optional[Literal["M", "O", "C"]] # M (Mandatory close), O (Open), C (Close)
    # options: Optional[int] # Unsure of purpose
    # ref: Optional[str]
    # ref2: Optional[str]
    # schedTime: Optional[float] # In the form YYYYMMDD.hhmmss # Unsure of formatting
    status: Optional[Literal[2]] # Only required in inactive orders (2 = Inactive)
    stopPriceInDec: Optional[int]
    stopType: Optional[Literal["L", "U", "D"]] # L (Stop loss), U (Up trigger), D (Down trigger), or blank (N/A) # Can ignore U and D
    subCondType: Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 11 (Stop loss by price), 14 (OCO by price), 16 (Trailing stop by price)
    # upLevelInDec: Optional[float]
    # upPriceInDec: Optional[float]
    # validDate: Optional[int] # YYYYMMDD

    @validator('priceInDec')
    def price_check(cls, price):
        if price <= 0: 
            raise ValueError('Price value should not be equal to or less than 0.')
        return price

    @validator('qty')
    def qty_check(cls, qty):
        if qty < 0: 
            raise ValueError('Quantity should be an integer and larger than 0.')
        return qty

    @root_validator()
    def stop_price_type_check(cls, order: Dict) -> Dict:
        condType = order.get("condType")
        subCondType = order.get("subCondType")
        stopPrice = order.get("stopPriceInDec")
        if ((condType == 1 or condType == 4 or condType == 6) or (subCondType != 0 and subCondType != 3)) and stopPrice is None:
            raise ValueError('Stop order should have a stop price.')
        return order

    # @validator('validDate')
    # def date_check(cls, date):
    #     if len(str(date)) != 8: 
    #         raise ValueError('validDate format is incorrect.')
    #     return date

class ChangeOrder(BaseModel):
    accNo: str
    accOrderNo: int # Collect from the order number within Get Account Order API or using the one displayed in Add Order
    buySell: Literal["B", "S"]
    prodCode: str
    sessionToken: str
    # sessionToken: Optional[str] # Set so it will be filled by system
    # downLevelInDec: Optional[float]
    # downPriceInDec: Optional[float]
    extOrderId: str # Need to use Get Account Order API to obtain before usage; now works every time without error (?)
    priceInDec: Optional[float]
    qty: Optional[int]
    # schedTime: Optional[float] # In the form YYYYMMDD.hhmmss # Unsure of formatting
    stopPriceInDec: Optional[int]
    # upLevelInDec: Optional[float]
    # upPriceInDec: Optional[float]
    # validDate: Optional[int] # YYYYMMDD

    @validator('priceInDec')
    def price_check(cls, price):
        if price <= 0: 
            raise ValueError('Price value should not be equal to or less than 0.')
        return price

    @validator('qty')
    def qty_check(cls, qty):
        if qty < 0: 
            raise ValueError('Quantity should be an integer and larger than 0.')
        return qty

    # @validator('validDate')
    # def date_check(cls, date):
    #     if len(str(date)) != 8: 
    #         raise ValueError('validDate format is incorrect.')
    #     return date

# For activate, deactivate and delete orders
class AccessOrder(BaseModel):
    accNo: str
    accOrderNo: int
    buySell: Literal["B", "S"]
    prodCode: str
    sessionToken: str
    # sessionToken: Optional[str] # Set so it will be filled by system
    extOrderId: str

# class MakeFuture(BaseModel):
#     buySell: Literal["B", "S"]
#     prodCode: str
#     qty: int
#     sessionToken: str
#     targetAccNo: str