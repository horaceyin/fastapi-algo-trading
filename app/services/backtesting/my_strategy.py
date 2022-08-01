from services.backtesting.sp_backtesting import SPBacktesting
from schemas.backtesting.backtesting_schemas import BacktestingModel

from services.backtesting.spbarfeed.sp_bar_feed import SpBarFeed
from services.sp_broker import SPBroker
from pyalgotrade.bar import Bars

class MyStrategy(SPBacktesting):
    def __init__(self, request: BacktestingModel):
        super().__init__(request) # Can access self.__sp_bar_feed and self.__sp_broker 
        # print(self.sp_bar_feed) # Cannot be self.sp_bar_feed() or TypeError will occur
        # print(self.getBroker()) # Cannot use getter class here # () to access functions inside getBroker # Same as self.sp_broker
        
        print(self.getBroker().get_portfolio_value) # Initially 1000000.0
        self.getBroker().get_portfolio_value = 2000000.0 # To set new portfolio_value
        print(self.getBroker().get_portfolio_value) # Now 2000000.0

    def onBars(self, bars: Bars): # ENTER USER'S OWN CODING HERE
        print("!!!!!!!!!!!!!!!!!!!!")
        # def __get_instrument(self, product_list, instrument):
        #     for i in range(len(product_list)):
        #         if product_list[i] == instrument:
        #             return instrument
        # self.__instrument = __get_instrument(product_list, instrument)
        # bar = bars[self.__instrument] # bars = current pyalgotrade.bar.Bars # Requires 1 product from product_list # self.__instrument is a string

    def onStart(self):
        print("start...............................................")

    def onFinish(self, bars):
        print("finish...............................................")
