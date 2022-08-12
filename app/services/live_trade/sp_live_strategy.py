from pyalgotrade.strategy import BaseStrategy # NEED TO CHANGE
from schemas.live_trading_schemas import GetTickerPriceModel

from services.live_trade.sp_live_trade_feed import SPLiveTradeFeed
from services.broker.sp_broker import SPBroker

class MyStrategy(BaseStrategy): # NEED TO CHANGE
    def __init__(self, request: GetTickerPriceModel):
        super().__init__(request) # 

    def onBars(self, bars: dict): # ENTER USER'S OWN CODING HERE
        # pyalgotrade  http://gbeced.github.io/pyalgotrade/docs/v0.20/html/index.html#
        super().onBars(bars)

    def onStart(self):
        print("start...............................................")

    def onFinish(self, bars):
        print("finish...............................................")
