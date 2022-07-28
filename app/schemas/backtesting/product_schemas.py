from typing import List, Optional, Union
from pydantic import BaseModel, validator, StrictInt
from schemas.backtesting.indicator_schemas import (
    SMA,
    EMA,
    WMA,
    MACD,
    ROC,
    RSI,
    BollingerBands
)
from schemas.backtesting.bar_summary_schemas import BarSummary

class Product(BaseModel):
    name: str
    indicators: List[Union[
        SMA,
        EMA,
        WMA,
        MACD,
        ROC,
        RSI,
        BollingerBands
    ]]
    # days: Optional[StrictInt] = 2
    # barSummary: BarSummary # Bar summarizes the trading activity during barSummary seconds

    # @validator('days')
    # def day_check(cls, day):
    #     if day < 0: raise ValueError('Days should be an integer and larger than 0.')
    #     return day