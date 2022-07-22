from dataclasses import field
import six, abc, pyalgotrade
from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from schemas.backtesting.backtesting_schemas import BacktestingModel

from pyalgotrade.broker import backtesting
from pyalgotrade.barfeed.csvfeed import BarFeed
from services.backtesting.spbarfeed.sp_live_trading_feed import SpBarFeed

# class SPBroker(backtesting.Broker):
#     def __init__(self, portfolio_value, live_trade=True) -> None:
#         super().__init__(portfolio_value)

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBacktesting(BacktestingStrategy, abc.ABC):
    
    def __init__(self, request: BacktestingModel, live_trade=False):
        self.__prod_indicator_list = request.prodCode
        self.__portfolio_value = request.portfolioValue
        self.__boundary_value = request.boundaryValue
        self.__days = request.days
        self.__bar_summary = request.barSummary

        self.product_list = self.__get_product(self.__prod_indicator_list) # create list: ['HSIM2', 'HSIZ4']
        # self.__indicator_list = request.indicator
        # self.__the_days_after = request.days
        # self.__barSummary = request.barSummary
        
        self.sp_bar_feed = SpBarFeed(self.__prod_indicator_list, self.__days, self.__bar_summary)
        # self.__sp_broker = SPBroker()
        super(SPBacktesting, self).__init__(self.sp_bar_feed)

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

    def __get_product(self, prod_indicator_list):
        if len(prod_indicator_list) == 0: return None

        product_list = [product.name for product in prod_indicator_list]

        return product_list

    @abc.abstractmethod
    def onBars(self, bars):
        return NotImplementedError

    def get_sp_data(self):
        pass