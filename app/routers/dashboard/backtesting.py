from fastapi import APIRouter, Depends, status
from schemas.backtesting_schemas import BacktestingMode
from services.backtesting_service import BacktestingService

@staticmethod
def print_msg():
    print("Calling at backtesting router.")

backtestingRouter = APIRouter(
    tags=['backTesting'],
    prefix='/backtesting',
    dependencies=[Depends(print_msg)]
)

@backtestingRouter.post('/', status_code=status.HTTP_200_OK)
async def do_backtesting(request: BacktestingMode):
    return BacktestingService.run_backtesting(request)