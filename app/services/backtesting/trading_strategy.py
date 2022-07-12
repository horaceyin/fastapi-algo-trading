import abc
import six
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

# @six.add_metaclass(metaclass=abc.ABC)
# class TradingStrategy(strategy.BacktestingStrategy):
    
#     def __init__(self, barFeed, cash_or_brk=1000000):
#         super().__init__(barFeed, cash_or_brk)

#     @abc.abstractmethod
#     def onBars(self, bars):
#         return NotImplementedError