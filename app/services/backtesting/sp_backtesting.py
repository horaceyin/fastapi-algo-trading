import abc
from pyalgotrade.strategy import BacktestingStrategy
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.spbarfeed.sp_bar_feed import SpBarFeed
from services.sp_broker import SPBroker

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
        self.sp_bar_feed = SpBarFeed(self.product_list, self.__days, self.__bar_summary) # SpBarFeed(barSummary, loadedBars=[], timezone = None, maxLen = None) # No __ in front to allow usage outside
        self.sp_broker = SPBroker(self.__portfolio_value, self.__boundary_value, self.sp_bar_feed, live_trade)
            # 
        super(SPBacktesting, self).__init__(self.sp_bar_feed, self.sp_broker) # BacktestingStrategy(barFeed, cash_or_brk=1000000)

    @property
    def get_prod_indicator_list(self):
        return self.__prod_indicator_list

    @get_prod_indicator_list.setter
    def get_prod_indicator_list(self, prod_code):
        self.__prod_indicator_list = prod_code

    @property
    def get_portfolio_value(self):
        return self.__portfolio_value

    @get_portfolio_value.setter
    def get_portfolio_value(self, port_val):
        if port_val > 0:
            if hasattr(self, 'sp_broker'):
                self.__portfolio_value = port_val
                self.sp_broker.get_portfolio_value(port_val)
            else:
                raise AttributeError(f'{type(self).__name__} does not have sp_broker attribute.')
        else:
            raise ValueError(f'portfolio should be larger than 0')

    @property
    def get_boundary_value(self):
        return self.__boundary_value

    @get_boundary_value.setter
    def get_boundary_value(self, bound_val):
        self.__boundary_value = bound_val

    @property
    def get_days(self):
        return self.__days

    @get_days.setter
    def get_days(self, days):
        self.__days = days

    # @property
    # def get_the_days_after(self):
    #     return self.__the_days_after

    # @get_the_days_after.setter
    # def get_the_days_after(self, days):
    #     self.__the_days_after = days

    @property
    def get_barSummary(self):
        return self.__barSummary

    @get_barSummary.setter
    def get_barSummary(self, bar_summary):
        self.__barSummary = bar_summary

    @property
    def get_position(self):
        return self.__position

    @get_position.setter
    def get_position(self, position):
        self.__position = position

    @property
    def get_live_trade(self):
        return self.__live_trade

    @get_live_trade.setter
    def get_live_trade(self, live_trade):
        self.__live_trade = live_trade

    @property
    def get_product_list(self):
        return self.product_list

    @get_product_list.setter
    def get_product_list(self, prod_list):
        self.product_list = prod_list

    @property
    def get_sp_bar_feed(self):
        return self.sp_bar_feed

    @get_sp_bar_feed.setter
    def get_sp_bar_feed(self, sp_bar_feed):
        self.sp_bar_feed = sp_bar_feed

    # getBroker already exists
    # @property
    # def get_sp_broker(self):
    #     return self.sp_broker

    # @get_sp_broker.setter
    # def get_sp_broker(self, sp_broker):
    #     self.sp_broker = sp_broker
    
    def __get_product(self, prod_indicator_list):
        if len(prod_indicator_list) == 0: return None

        product_list = [product.name for product in prod_indicator_list]

        return product_list

    # @abc.abstractmethod
    # def onBars(self, bars, product_list, instrument): # SHOULD BE IMPLEMENTED BY FUTURE USERS
    #     return NotImplementedError

    def get_sp_data(self):
        pass