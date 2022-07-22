from typing import List, Optional, Union
from pydantic import BaseModel, validator, StrictInt
from schemas.backtesting.indicator_schemas import (
    SMA,
    EMA,
    WMA,
    MACD,
    ROC,
    RSI,
    BollingerBands,
    StochasticOscillator
)

class Product(BaseModel):
    name: str
    indicator: List[Union[
        SMA,
        EMA,
        WMA,
        MACD,
        ROC,
        RSI,
        BollingerBands,
        StochasticOscillator
    ]]

    # @validator('days')
    # def day_check(cls, day):
    #     if day < 0: raise ValueError('Days should be an integer and larger than 0.')
    #     return day