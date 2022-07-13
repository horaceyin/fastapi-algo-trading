import six, abc, pyalgotrade
from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

@six.add_metaclass(metaclass=abc.ABCMeta)
class SPBacktesting(BacktestingStrategy):
    
    def __init__(self, barFeed, cash_or_brk=1000000):
        super(SPBacktesting, self).__init__(barFeed, cash_or_brk)

    @abc.abstractmethod
    def onBars(self, bars):
        return NotImplementedError