from dataclasses import field
import abc
from pyalgotrade.strategy import BacktestingStrategy
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.spbarfeed.sp_live_trading_feed import SpBarFeed
from services.sp_broker import SPBroker

# class SPBroker(backtesting.Broker):
#     def __init__(self, portfolio_value, live_trade=True) -> None:
#         super().__init__(portfolio_value)

# class SpBarFeed(BarFeed):
#     def __init__(self, frequency, maxLen=None):
#         super().__init__(frequency, maxLen)

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBacktesting(BacktestingStrategy, abc.ABC):
    
    def __init__(self, request: BacktestingModel):
        self.__prod_indicator_list = request.prodCode
        self.__portfolio_value = request.portfolioValue
        self.__boundary_value = request.boundaryValue
        self.__live_trade = request.liveTrade
        self.__days = request.days
        self.__bar_summary = request.barSummary
        # May need userId, password, and targetAcc

        self.__position = None
        self.product_list = self.__get_product(self.__prod_indicator_list) # create list: ['HSIM2', 'HSIZ4']
        self.__sp_bar_feed = SpBarFeed(self.__bar_summary, self.__days) # SpBarFeed(barSummary, loadedBars=[], timezone = None, maxLen = None)
        self.__sp_broker = SPBroker(self.__portfolio_value, self.__boundary_value, self.__sp_bar_feed, self.__live_trade)
            # 
        super(SPBacktesting, self).__init__(self.__sp_bar_feed, self.__sp_broker) # BacktestingStrategy(barFeed, cash_or_brk=1000000)

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

    @property
    def get_live_trade(self):
        return self.__live_trade

    @get_live_trade.setter
    def get_live_trade(self, live_trade):
        self.__live_trade = live_trade
    
    def __get_product(self, prod_indicator_list):
        if len(prod_indicator_list) == 0: 
            return None
        product_list = [product.name for product in prod_indicator_list]
        return product_list

    @abc.abstractmethod
    # def onBars(self, bars):
    def onBars(self, bars, product_list, instrument): # ASK HORACE ON HOW THIS WORKS
        def __get_instrument(self, product_list, instrument):
            for i in range(len(product_list)):
                if product_list[i] == instrument:
                    return instrument
        self.__instrument = __get_instrument(product_list, instrument)
        bar = bars[self.__instrument] # bars = current pyalgotrade.bar.Bars
        return NotImplementedError

    def get_sp_data(self):
        pass