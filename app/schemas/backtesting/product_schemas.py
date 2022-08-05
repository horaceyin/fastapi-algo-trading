from typing import List, Optional, Union
from pydantic import BaseModel
# from schemas.backtesting.indicator_schemas import (
#     SMA,
#     EMA,
#     WMA,
#     MACD,
#     ROC,
#     RSI,
#     BollingerBands
# )

"""
    The model allows user specifying which indicators taken. The sp_backtesting.py will create the indicators object to user.
    But, there is an issue. When the backend receives run_backtesting request, backtesting starts immediately. Also, 
    user must define their own trading logic in onBar function and also the indicators object before sending a request. 
    Because onBar function should be overwritten before starting backtesting.
    The decision making (enterlong, entershort) basically depend on the result calculated from the indicators. So, indicators should be
    defined by user, not the sp_backtesting.py
"""
class Product(BaseModel):
    name: str
    # indicators: List[Union[
    #     SMA,
    #     EMA,
    #     WMA,
    #     MACD,
    #     ROC,
    #     RSI,
    #     BollingerBands
    # ]]