from fastapi import APIRouter, Depends, status
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.backtesting_service import BacktestingService

# testing msg when this router is called
@staticmethod
def print_msg():
    print("Calling at backtesting router.")

# set up router
backtestingRouter = APIRouter(
    tags=['Backtesting'],
    prefix='/backtesting',
    dependencies=[Depends(print_msg)]
)

# the post method for doing backtesting
# starting with host/backtesting/
@backtestingRouter.post('/', status_code=status.HTTP_200_OK)
async def do_backtesting(request: BacktestingModel):
    return BacktestingService.run_backtesting(request)