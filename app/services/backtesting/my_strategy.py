from services.backtesting.sp_backtesting import SPBacktesting
from schemas.backtesting.backtesting_schemas import BacktestingModel

from services.backtesting.spbarfeed.sp_bar_feed import SpBarFeed
from services.sp_broker import SPBroker

class MyStrategy(SPBacktesting):
    def __init__(self, request: BacktestingModel):
        super().__init__(request) # Can access self.__sp_bar_feed and self.__sp_broker 
        print(self.sp_bar_feed) # Cannot be self.sp_bar_feed() or TypeError will occur
        print(self.sp_broker) # Cannot use getter class here
        # broke = self.getBroker
        # print(broke)
        # print(broke.get_portfolio_value)

    # def onBars(self): # ENTER USER'S OWN CODING HERE
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     self.enterLong()
    #     # def __get_instrument(self, product_list, instrument):
    #     #     for i in range(len(product_list)):
    #     #         if product_list[i] == instrument:
    #     #             return instrument
    #     # self.__instrument = __get_instrument(product_list, instrument)
    #     # bar = bars[self.__instrument] # bars = current pyalgotrade.bar.Bars # Requires 1 product from product_list # self.__instrument is a string
