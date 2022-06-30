from os import environ
import json
from dotenv import load_dotenv
from schemas.backtesting_schemas import BacktestingModel

load_dotenv()
ENDPOINT = environ['SP_END_POINT']

class BacktestingService:
    def __init__(self):
        pass

    @staticmethod
    def run_backtesting(request: BacktestingModel):
        print(request)
        errMsg = ''
        return json.dumps({'msg': 'from backtesting.'})
        # write backtesting code here
        
        #if exception rasied,
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)