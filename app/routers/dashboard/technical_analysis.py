from fastapi import APIRouter, Depends, status
from schemas.technical_analysis_schemas import GetDoneTradeModel
from services.report_service import Report
from services.technical_analysis_service import PnLService
from datetime import datetime

# testing msg when this router is called
@staticmethod
def print_msg():
    print("Calling at technical analysis router.")

# set up router
taRouter = APIRouter(
    tags=['Technical analysis'],
    prefix='/ta',
    dependencies=[Depends(print_msg)]
)

# the post method for geting profit and loss of done trades
# starting with host/get-pnl/
@taRouter.post('/get-pnl', status_code=status.HTTP_200_OK)
async def get_pnl_for_report_analysis(request: GetDoneTradeModel):
    accName = request.targetAccNo
    pnlCal = PnLService(accName)
    return pnlCal.get_pnl(request)

# the post method for generating done trades report
# starting with host/report/
@taRouter.post('/report', status_code=status.HTTP_200_OK)
async def done_trade_report_analysis(request: GetDoneTradeModel):
    accName = request.targetAccNo
    date = datetime.now()
    date = date.strftime('%Y-%m-%d')
    pnlReport = Report(accName, date)
    return pnlReport.get_pnl(request)
