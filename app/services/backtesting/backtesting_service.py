from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.sma.sma_backtest_service import sma_backtest
from services.backtesting.sma.sma_login_details import portSize
from services.backtesting.my_strategy import MyStrategy

class BacktestingService:
    def __init__(self):
        pass

    @staticmethod
    def run_backtesting(request: BacktestingModel): # Make request that follows the BacktestingModel format
        """
        {
            "prodCode": [
                {
                    "name": "string",
                    "indicator": [
                        {
                        "maxLen": 0,
                        "indicatorName": "sma",
                        "period": 10
                        },
                        {
                        "maxLen": 0,
                        "indicatorName": "ema",
                        "period": 10
                        }
                    ]
                }
            ],
            "portfolioValue": 1000000,
            "boundaryValue": 0,
            "days": 2,
            "barSummary": {
                "day": false,
                "hour": false,
                "minute": false,
                "second": true,
                "input_time": 5
            }
        }
        """
        # return json.dumps({'msg': 'from backtesting.'}) # Result given
        # write backtesting code here

        # Reference this to make broker class; may not be neccessary
        # prodCode = request.prodCode
        # userid = request.userid
        # password = request.password
        # targetAcc = request.targetAcc
        # portfolioValue = request.portfolioValue
        # boundaryValue = request.boundaryValue
        # barSummary = request.barSummary
        # try: # Default value should be the user's portfolio size, if it exists
        #     testportfolio = portSize(userid, password, targetAcc).loginData()
        # except: 
        #     print("Account invalid, using 10000000 as sample portfolio size")
        #     testportfolio = 10000000
        # if portfolioValue > 0: # Proper portfolio value is given
        #     backtestValue = portfolioValue
        # else:
        #     backtestValue = testportfolio 
        
        # return sma_backtest(prodCode, 1, 5, 160, True, backtestValue, barSummary, boundaryValue).start_backtesting(request) 

        # sma_backtest(instrument, day, second, smaPeriod, plot, startcash, barsum, boundaryValue)
        # May need to add timeframe and method for data collection
        # Cannot test code due to errors
        # Build such that type of backtest can be changed

        my_strat = MyStrategy(request)
        return {'report': "data"}

        # #if exception rasied,
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)
