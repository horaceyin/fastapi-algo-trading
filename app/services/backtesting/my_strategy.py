from services.backtesting.sp_backtesting import SPBacktesting
from schemas.backtesting.backtesting_schemas import BacktestingModel

class MyStrategy(SPBacktesting):
    def __init__(self, request: BacktestingModel):
        super(MyStrategy, self).__init__(request)
        
        print(self.__sp_bar_feed)
        print(self.__sp_broker)

    def onBars(self, bars):
        print("!!!!!!!")
