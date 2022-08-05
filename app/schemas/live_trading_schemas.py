from typing import Optional
from pydantic import BaseModel

class GetTickerPriceModel(BaseModel):
    userId: str
    spServerKey: str
    sessionTime: str