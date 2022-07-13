from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, root_validator, validator

class TimeConverter(Enum):
    DAY = 86400
    HOUR = 3600
    MINUTE = 60
    SECOND = 1


class IndicatorName(str, Enum):
    SMA = 'sma'
    WMA = 'wma'
    MACD = 'macd'
    ROC = 'roc'
    RSI = 'rsi'
    BOLLINGER = 'bollinger bands'
    
class Indicator(BaseModel):
    indicatorName: IndicatorName
    param: int

class BarSummary(BaseModel):
    day: Optional[bool] = False
    hour: Optional[bool] = False
    minute: Optional[bool] = False
    second: Optional[bool] = True
    input_time: int = 5

    @root_validator
    def check_exclusive(cls, values):
        day, hour, mins, sec = values.get('day'), values.get('hour'), values.get('minute'), values.get('second')
        true_count = 0
        bar_summary = [day, hour, mins, sec]
        if True not in bar_summary: raise ValueError('Please select ones of the bar summary.')

        for choice in bar_summary:
            if choice is True: true_count = true_count + 1

        if true_count > 1: raise ValueError('Only one bar summary should be selected.')

        input_time = values.get('input_time')
        bar_type = 'second'
        time_in_sec = [input_time]

        if day: 
            time_in_sec[0] = input_time * TimeConverter.DAY
            bar_type = 'day'
        elif hour:
            time_in_sec[0] = input_time * TimeConverter.HOUR
            bar_type = 'hour'
        elif mins: 
            time_in_sec[0] = input_time * TimeConverter.MINUTE
            bar_type = 'minute'

        field = cls.__fields__[bar_type]
        if time_in_sec[0] % 5 != 0: raise ValueError(f'{input_time} ({field.name}) is not supported.')

        return values

class BacktestingModel(BaseModel):
    prodCode: List[str]
    indicator: List[Indicator]
    days: Optional[int] = 2
    portfolioValue: int = 1000000 # avFund # Default value should be the user's portfolio size
    boundaryValue: Optional[int] = 0
    barSummary: BarSummary # Bar summarizes the trading activity during barSummary seconds
    # userid: Optional[str]
    # password: Optional[str]
    # targetAcc: Optional[str] = "SPTEST"

    @validator('days')
    def day_check(cls, day):
        if day < 0 or day > 7: raise ValueError('Days should be in range of 0 ~ 7.')
        return day

    @validator('portfolioValue')
    def portfolio_check(cls, portfolio_val):
        if portfolio_val <= 0: raise ValueError('Portfolio value should not be equal to or less than 0.')
        return portfolio_val

    @validator('boundaryValue')
    def boundary_check(cls, boundary, values):
        if 'portfolioValue' in values and boundary >= values.get('portfolioValue'):
            raise ValueError('Boundary value should not be equal to or greater than portfolio value.')
        elif boundary < 0:
            raise ValueError('Boundary value should not be less than 0.')
        return boundary
