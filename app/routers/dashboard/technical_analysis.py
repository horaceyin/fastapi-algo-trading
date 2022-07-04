from fastapi import APIRouter, Depends, status
from schemas.technical_analysis_schemas import GetDoneTradeModel
from services.technical_analysis_service import TaService

@staticmethod
def print_msg():
    print("Calling at technical analysis router.")

taRouter = APIRouter(
    tags=['Technical analysis'],
    prefix='/ta',
    dependencies=[Depends(print_msg)]
)

@taRouter.post('/get-pnl', status_code=status.HTTP_200_OK)
async def get_pnl_for_report_analysis(request: GetDoneTradeModel):
    accName = request.targetAccNo
    taHelper = TaService(accName)
    return taHelper.get_pnl(request)

@taRouter.post('/report', status_code=status.HTTP_200_OK)
async def done_trade_report_analysis():
    pass
