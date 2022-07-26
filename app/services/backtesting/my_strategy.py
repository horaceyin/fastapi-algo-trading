from services.backtesting.sp_backtesting import SPBacktesting
from schemas.backtesting.backtesting_schemas import BacktestingModel

class MyStrategy(SPBacktesting):
    def __init__(self, request: BacktestingModel):
        super(MyStrategy, self).__init__(request)
        
        print(self.__sp_bar_feed)
        print(self.__sp_broker)

    def onBars(self, bars):
        print("!!!!!!!")
        bar = bars[self.__instrument] # Requires 1 product from product_list # self.__instrument is a string
