from fastapi import APIRouter, Depends, status, Request
from schemas.technical_analysis_schemas import GetDoneTradeModel
from services.report_service import Report
from services.technical_analysis_service import PnLService
from services.contract_size_service import ContractSize
from datetime import datetime
from fastapi.templating import Jinja2Templates
from core import TEMPLATES_PATH
from fastapi.responses import HTMLResponse

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
    report = pnlReport.get_report(request)
    return report
    # return templates.TemplateResponse('report.html', {'report': report}) # ValueError: context must include a "request" key

# ****************************** Want to render HTML page **********************************************
# @taRouter.get('/get-report', response_class=HTMLResponse)
# async def get_done_trade_report_analysis(request: Request):
#     return templates.TemplateResponse('report.html', {'request': request}) # Second parameter -> Information to be passed through for template