import json
from os import environ
from dotenv import load_dotenv
from fastapi import HTTPException, status
from schemas.technical_analysis_schemas import GetDoneTradeModel

load_dotenv()
ENDPOINT = environ['SP_END_POINT']

class TaService:
    def __init__(self):
        pass

    @staticmethod
    def run_done_trade_analysis(request: GetDoneTradeModel):
        myUrl = ENDPOINT + "/apiCustomer/reporting/doneTrade"
        print(request)
        errMsg = ''
        return json.dumps({'msg': 'from done trade analysis.'})
        # write performance analysis code here
        
        # if exception rasied,
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)