from common.common_helper import CommonHelper
from schemas.technical_analysis_schemas import GetDoneTradeModel

class TaService:
    def __init__(self):
        pass

    @staticmethod
    def run_done_trade_analysis(request: GetDoneTradeModel):
        myUrl = "/apiCustomer/reporting/doneTrade"
        return CommonHelper.postUrl(requestUrl=myUrl, params=request)
        # print(request)
        # errMsg = ''
        # return json.dumps({'msg': 'from done trade analysis.'})
        # write performance analysis code here
        
        # if exception rasied,
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)