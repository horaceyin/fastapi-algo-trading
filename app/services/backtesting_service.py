from os import environ
import json
from dotenv import load_dotenv
from fastapi import HTTPException, status
from schemas.backtesting_schemas import BacktestingModel
from sma_simple_strat import *

load_dotenv()
ENDPOINT = environ['SP_END_POINT']

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
        return start_backtesting(BacktestingModel.prodCode, 4, 120, 80, True, BacktestingModel.portfolioValue)

        #if exception rasied,
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)