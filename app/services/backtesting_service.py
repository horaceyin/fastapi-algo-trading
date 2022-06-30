from os import environ
import json
from schemas.backtesting_schemas import BacktestingModel
from services.sma_simple_strat import sma_backtest

class BacktestingService:
    def __init__(self):
        pass

    @staticmethod
    def run_backtesting(request: BacktestingModel):
        print(request)
        errMsg = ''
        # return json.dumps({'msg': 'from backtesting.'}) # Result given
        # write backtesting code here
        
        # ModuleNotFoundError: No module named 'sma_simple_strat'
        return sma_backtest(BacktestingModel.prodCode, 2, 120, 80, True, BacktestingModel.portfolioValue).start_backtesting() 
        # May need to add timeframe and method for data collection
        # AttributeError: type object 'BacktestingModel' has no attribute 'prodCode'

        #if exception rasied,
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)