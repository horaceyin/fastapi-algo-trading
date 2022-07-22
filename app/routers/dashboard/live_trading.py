from turtle import st
from fastapi import APIRouter, Depends, Path, status, WebSocket, Cookie, Query
from typing import Union
from fastapi.responses import HTMLResponse

@staticmethod
def print_msg():
    print('Calling at live trading router.')

live_trading_router = APIRouter(
    tags=['live trading'],
    prefix='/live-trading',
    dependencies=[Depends(print_msg)]
)


@live_trading_router.get('/')
async  def live_trading():
    return {'msg': 'live trading router.'}
# async def read_items(items: str, xx: Union[str, None] = Cookie(default=None)):
#     yy = xx.encode(items)
#     return {"ads_id": yy}