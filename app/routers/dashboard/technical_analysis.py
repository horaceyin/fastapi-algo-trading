from fastapi import APIRouter, Depends, status
from schemas.technical_analysis_schemas import GetDoneTradeModel
from services.report_service import Report
from services.technical_analysis_service import PnLService
from services.contract_size_service import ContractSize
from datetime import datetime
from fastapi.templating import Jinja2Templates
from core import TEMPLATES_PATH

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

templates = Jinja2Templates(directory=str(TEMPLATES_PATH))

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
    return pnlReport.get_report(request)

@taRouter.get('/get-report', status_code=status.HTTP_200_OK())
async def get_done_trade_report_analysis(request: GetDoneTradeModel):
    return templates.TemplateResponse('report.html', {'request': request})