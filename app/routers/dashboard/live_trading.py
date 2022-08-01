from fastapi import APIRouter, Depends, Path, Request, status, WebSocket, Cookie, Query
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core import TEMPLATES_PATH

@staticmethod
def print_msg():
    print('Calling at live trading router.')

live_trading_router = APIRouter(
    tags=['live trading'],
    prefix='/live-trading',
    dependencies=[Depends(print_msg)]
)

templates = Jinja2Templates(directory=str(TEMPLATES_PATH))

@live_trading_router.get('/', response_class=HTMLResponse)
async  def show_live_trading_page(request: Request):
    return templates.TemplateResponse('backtesting.html', {'request': request})
# async def read_items(items: str, xx: Union[str, None] = Cookie(default=None)):
#     yy = xx.encode(items)
#     return {"ads_id": yy}