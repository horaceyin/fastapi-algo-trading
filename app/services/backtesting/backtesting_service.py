from os import environ
import json
from schemas.backtesting_schemas import BacktestingModel
from services.backtesting.sma.sma_backtest_service import sma_backtest
from services.backtesting.sma.sma_login_details import portSize

class BacktestingService:
    def __init__(self):
        pass

    @staticmethod
    def run_backtesting(request: BacktestingModel): # Make request that follows the BacktestingModel format
        print(request)
        errMsg = ''
        # return json.dumps({'msg': 'from backtesting.'}) # Result given
        # write backtesting code here
        prodCode = request.prodCode
        userid = request.userid
        password = request.password
        targetAcc = request.targetAcc
        portfolioValue = request.portfolioValue
        try: # Default value should be the user's portfolio size, if it exists
            testportfolio = portSize(userid, password, targetAcc).loginData()
        except: 
            print("Account invalid, using 10000000 as sample portfolio size")
            testportfolio = 10000000
        if portfolioValue > 0: # Proper portfolio value is given
            backtestValue = portfolioValue
        else:
            backtestValue = testportfolio 
        barSummary = request.barSummary
        boundaryValue = request.boundaryValue
        return sma_backtest(prodCode, 1, 5, 160, True, backtestValue, barSummary, boundaryValue).start_backtesting(request) 
        # May need to add timeframe and method for data collection
        # Cannot test code due to errors
        # Build such that type of backtest can be changed

        #if exception rasied,
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)
