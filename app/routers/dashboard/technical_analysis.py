from fastapi import APIRouter, Depends, status, Request, WebSocket, Cookie, Query
from fastapi.responses import JSONResponse
from schemas.technical_analysis_schemas import GetDoneTradeModel
from services.report_service import Report
from services.technical_analysis_service import PnLService
from services.contract_size_service import ContractSize
from datetime import datetime
from fastapi.templating import Jinja2Templates
from core import TEMPLATES_PATH
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from json import dumps
from typing import Union

# Testing msg when this router is called
@staticmethod
def print_msg():
    print("Calling at technical analysis router.")

# Set up router
taRouter = APIRouter(
    tags=['Technical analysis'],
    prefix='/ta',
    dependencies=[Depends(print_msg)]
)

templates = Jinja2Templates(directory=str(TEMPLATES_PATH))

# Post method for geting profit and loss of done trades
# Starting with host/get-pnl/
@taRouter.post('/get-pnl', status_code=status.HTTP_200_OK)
async def get_pnl_for_report_analysis(request: GetDoneTradeModel):
    accName = request.targetAccNo
    pnlCal = PnLService(accName)
    pnl = jsonable_encoder(pnlCal.get_pnl(request))
    json_pnl = dumps(pnl)
    return JSONResponse(content=json_pnl)

# Post method for generating done trades report
# Starting with host/report/
@taRouter.post('/get-report', status_code=status.HTTP_200_OK)
# async def done_trade_report_analysis(request: GetDoneTradeModel, httpRequest: Request):
async def done_trade_report_analysis(request: GetDoneTradeModel):
    accName = request.targetAccNo
    date = datetime.now()
    date = date.strftime('%Y-%m-%d')
    pnlReport = Report(accName, date)
    report = jsonable_encoder(pnlReport.get_report(request)) # make sure its a dict or list (json-compatible type)
    json_report = dumps(report) # json string
    return JSONResponse(content=json_report)
    # return templates.TemplateResponse('report.html', {'report': report}) # ValueError: context must include a "request" key

# ****************************** Want to render HTML page **********************************************
# @taRouter.get('/get-report')
# async def get_done_trade_report_analysis(request: GetDoneTradeModel, httpRequest : Request):
@taRouter.get('/report', response_class=HTMLResponse)
async def get_report_page(httpRequest: Request): # Not used, may need to be deleted
    # e.g. 
    # "total": {
    #     "Total trades": 19,
    #     "Avg. Profit": -66.76315789473647,
    #     "Profits. std. dev.": 119.08781794149354,
    #     "Min. Profit": -400.0,
    #     "Max. Profit": 9.0,
    #     "Avg. Return": -6.7,
    #     "Return std. dev.": 0.048762200132775824,
    #     "Max. Return": 2.4946641904814704,
    #     "Min. Return": -11.616989449226812,
    #     "Overall P/L Ratio": -0.09278752436647227,
    #     "Average Profitability per Trade": 68.23684210526278
    # },
    # "profitable": {
    #     "Profitable trades": 2,
    #     "Avg. profit": 7.0,
    #     "Profits. std. dev.": 2.8284271247461903,
    #     "Min. Profit": 5.0,
    #     "Max. Profit": 9.0,
    #     "Avg. Return": 2.4,
    #     "Return std. dev.": 0.0006926963170879234,
    #     "Max. Return": 2.4946641904814704,
    #     "Min. Return": 2.396702137858307
    # },
    # "unprofitable": {
    #     "Unprofitable trades": 17,
    #     "Avg. Loss": -75.4411764705878,
    #     "Losses. std. dev.": 123.26397178493042,
    #     "Min. Loss": -400.0,
    #     "Max. Loss": -17.5,
    #     "Avg. Return": -7.7,
    #     "Return std. dev.": 0.038960076156598314,
    #     "Max. Return": -1.7008868910217472,
    #     "Min. Return": -11.616989449226812
    # }
    
    # report = done_trade_report_analysis(request)
    return templates.TemplateResponse('report.html', {'request': httpRequest}) # Second parameter -> Information to be passed through for template # Will retrieve GetDoneTradeModel by function in HTML

# async def get_cookie_or_token(
#     websocket: WebSocket,
#     session: Union[str, None] = Cookie(default=None),
#     token: Union[str, None] = Query(default=None),
# ):
#     if session is None and token is None:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token

