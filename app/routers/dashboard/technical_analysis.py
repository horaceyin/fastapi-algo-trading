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

@taRouter.post('/', status_code=status.HTTP_200_OK)
async def done_trade_report_analysis(request: GetDoneTradeModel):
    return TaService.run_done_trade_analysis(request)
