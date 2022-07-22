import abc
from enum import Enum
from typing import List, Union
from pydantic import BaseModel, StrictFloat, root_validator, validator, StrictInt
from pyalgotrade.dataseries import DEFAULT_MAX_LEN

def period_checking(period):
    if period < 1:
        raise ValueError('Period should not be less than 1')
    return period

# class IndicatorName(str, Enum):
#     SMA = 'sma',
#     EMA = 'ema'
#     WMA = 'wma'
#     MACD = 'macd'
#     ROC = 'roc'
#     RSI = 'rsi'
#     BOLLINGER = 'bollinger bands'
#     stoch = 'stochastic oscillator'

class Indicator(BaseModel, abc.ABC):
    maxLen: int = None
    
    @validator('maxLen')
    def max_len_checking(cls, max_len):
        if max_len is not None:
            assert (max_len > 1 or max_len <= DEFAULT_MAX_LEN), f'Max length should be in range of 1 ~ {DEFAULT_MAX_LEN}'
        return max_len

class SMA(Indicator):
    indicatorName: str = 'sma'
    period: StrictInt = 10
    _period = validator('period', allow_reuse=True)(period_checking)

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'sma', ValueError(f'indicatorName must be "sma"')
        return indicatorName
    
class EMA(Indicator):
    indicatorName: str = 'ema'
    period: StrictInt = 10
    _period = validator('period', allow_reuse=True)(period_checking)

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'ema', ValueError(f'indicatorName must be "ema"')
        return indicatorName

class WMA(Indicator):
    indicatorName: str = 'wma'
    weight: List[Union[StrictInt, StrictFloat]] = [5, 4, 3, 2, 1]

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'wma', ValueError(f'indicatorName must be "wma"')
        return indicatorName

class MACD(Indicator):
    indicatorName: str = 'macd'
    fastEMA: StrictInt = 12
    slowEMA: StrictInt = 26
    signalEMA: StrictInt = 9

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'macd', ValueError(f'indicatorName must be "macd"')
        return indicatorName

    @root_validator
    def value_validation(cls, values):
        fast_ema = values.get('fastEMA')
        slow_ema = values.get('slowEMA')
        signal_ema = values.get('signalEMA')
        
        assert fast_ema > 1, ValueError(f'fastEMA must larger than 1. Now: {fast_ema}')
        assert slow_ema > 1, ValueError(f'slowEMA must larger than 1. Now: {slow_ema}')
        assert signal_ema > 1, ValueError(f'signalEMA must larger than 1. Now: {signal_ema}')
        assert fast_ema < slow_ema, ValueError(f'fastEMA must be less than slowEMA.')
        return values

class ROC(Indicator):
    indicatorName: str = 'roc'
    valuesAge: StrictInt = 12
    @validator('valuesAge')
    def validation(cls, valuesAge):
        assert valuesAge > 0, ValueError(f'valuesAge must be larger than 0.')
        return valuesAge

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'roc', ValueError(f'indicatorName must be "roc"')
        return indicatorName

class RSI(Indicator):
    indicatorName: str = 'rsi'
    period: StrictInt = 14
    _period = validator('period', allow_reuse=True)(period_checking)

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'rsi', ValueError(f'indicatorName must be "rsi"')
        return indicatorName

class BollingerBands(Indicator):
    indicatorName: str = 'bollinger bands'
    period: StrictInt = 20
    numStdDev: Union[int, float] = 2
    _period = validator('period', allow_reuse=True)(period_checking)
    
    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'bollinger bands', ValueError(f'indicatorName must be "bollinger bands"')
        return indicatorName

    @validator('numStdDev')
    def sd_validator(cls, numStdDev):
        assert numStdDev > 0, ValueError(f'numStdDev must be larger than 0')
        return numStdDev
    
class StochasticOscillator(Indicator):
    indicatorName: str = 'stochastic oscillator'
    period: StrictInt = 14
    dSMAPeriod: StrictInt = 3
    _period = validator('period', allow_reuse=True)(period_checking)

    @validator('indicatorName')
    def name_validation(cls, indicatorName):
        assert indicatorName == 'stochastic oscillator', ValueError(f'indicatorName must be "stochastic oscillator"')
        return indicatorName

    @validator('dSMAPeriod')
    def validation(cls, dSMAPeriod):
        assert dSMAPeriod > 1, ValueError(f'valuesAge must be larger than 1.')
        return dSMAPeriod