from services.backtesting.sp_backtesting import SPBacktesting
from schemas.backtesting.backtesting_schemas import BacktestingModel

class MyStrategy(SPBacktesting):
    def __init__(self, request: BacktestingModel):
        super(MyStrategy, self).__init__(request)
        
        print(self.sp_bar_feed)
        # print sp broker here.

    def onBars(self, bars):
        print("!!!!!!!")