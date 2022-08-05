from fastapi import APIRouter, Depends, status, Request
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.backtesting_service import BacktestingService
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core import TEMPLATES_PATH, STATIC_PATH

# Testing msg when this router is called
@staticmethod
def print_msg():
    print("Calling at backtesting router.")

# Set up router
backtestingRouter = APIRouter(
    tags=['Backtesting'],
    prefix='/backtesting',
    dependencies=[Depends(print_msg)]
)

templates = Jinja2Templates(directory=str(TEMPLATES_PATH)) # Link to html from templates folder

# backtestingRouter.mount('/static', StaticFiles(directory=str(STATIC_PATH)), name='static')
# print(backtestingRouter.routes[0].url_path_for('/ static'), "!!!!!!!!!!!!!!!!!!!!!!!!!!")

@backtestingRouter.get('/', response_class=HTMLResponse)
async def show_backtesting_page(request: Request):
    print(request.headers)
    return templates.TemplateResponse('backtesting.html', {'request': request})

# Post method for doing backtesting
# Starting with host/backtesting/
@backtestingRouter.post('/run', status_code=status.HTTP_200_OK)
async def do_backtesting(request: BacktestingModel):
    return BacktestingService.run_backtesting(request)