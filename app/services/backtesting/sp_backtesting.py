from typing import List
import xxlimited
import six, abc, pyalgotrade
from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from schemas.backtesting.backtesting_schemas import BacktestingModel
from sp_indicators import SPIndicators

from pyalgotrade.broker import backtesting
from pyalgotrade.barfeed.csvfeed import BarFeed

class SPBroker(backtesting.Broker):
    def __init__(self, portfolio_value, live_trade=True) -> None:
        super().__init__(portfolio_value)

class SPBarFeed(BarFeed):
    def __init__(self, frequency, maxLen=None):
        super().__init__(frequency, maxLen)

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBacktesting(BacktestingStrategy, abc.ABC):
    
    def __init__(self, request: BacktestingModel):
        self.__prod_list = request.prodCode
        self.__indicator_list = request.indicator
        self.__portfolio_value = request.portfolioValue
        self.__boundary_value = request.boundaryValue
        self.__the_days_after = request.days
        self.__barSummary = request.barSummary
        
        self.__sp_bar_feed = SPBarFeed()
        self.__sp_broker = SPBroker()
        super(SPBacktesting, self).__init__(self.__sp_bar_feed, self.__sp_broker)

    @property
    def get_prod_list(self):
        return self.__prod_list

    @get_prod_list.setter
    def get_prod_list(self, prod_code):
        self.__prod_list = prod_code

    @property
    def get_indicator_list(self):
        return self.__indicator_list

    @get_indicator_list.setter
    def get_indicator_list(self, indicator):
        self.__indicator_list = indicator

    @property
    def get_portfolio_value(self):
        return self.__portfolio_value

    @get_portfolio_value.setter
    def get_portfolio_value(self, val):
        self.__portfolio_value = val

    @property
    def get_boundary_value(self):
        return self.__boundary_value

    @get_boundary_value.setter
    def get_boundary_value(self, val):
        self.__boundary_value = val

    @property
    def get_the_days_after(self):
        return self.__the_days_after

    @get_the_days_after.setter
    def get_the_days_after(self, days):
        self.__the_days_after = days

    @property
    def get_barSummary(self):
        return self.__barSummary

    @get_barSummary.setter
    def get_barSummary(self, bar_summary):
        self.__barSummary = bar_summary
    
    @abc.abstractmethod
    def onBars(self, bars):
        return NotImplementedError

    def get_sp_data(self):
        pass