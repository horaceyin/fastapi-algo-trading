import json
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.sma_backtest_service import sma_backtest

class BacktestingService:
    def __init__(self):
        pass

    @staticmethod
    def run_backtesting(request: BacktestingModel): # Make request that follows the BacktestingModel format
        """
        {
            "prodCode": [
                "string"
            ],
            "indicator": [
                {
                "indicatorName": "sma",
                "param": 0
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
        return request


        # # return json.dumps({'msg': 'from backtesting.'}) # Result given
        # # write backtesting code here
        # productCode = request.prodCode
        # portfValue = request.portfolioValue
        # return sma_backtest(productCode, 2, 120, 80, True, portfValue, 1).start_backtesting(request) 
        # # May need to add timeframe and method for data collection