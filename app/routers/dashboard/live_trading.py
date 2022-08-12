from operator import truediv
from fastapi import APIRouter, Depends, Path, Request, status, WebSocket, Cookie, Query
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from core import TEMPLATES_PATH, config
from schemas.live_trading_schemas import GetTickerPriceModel
from core.config import SP_PRICE_SERVER_HOST, SP_PRICE_SERVER_PORT
import socket
import time
import sys

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
async def show_live_trading_page(request: Request):
    return templates.TemplateResponse('live_trading.html', {'request': request})

@live_trading_router.post('/subscribe-ticker-price')
async def get_ticker_price(request: GetTickerPriceModel):
    userId = request.userId
    spServerKey = request.spServerKey
    sessionTime = request.sessionTime
    prodCode = request.prodCode

    my_msg = f'4104,0,{userId},{spServerKey},3,8.7,1.0,1.0,SP_F,{sessionTime},0\r\n'
    my_msg_1 = f'4107,0,{prodCode},0,1,0\r\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((SP_PRICE_SERVER_HOST, SP_PRICE_SERVER_PORT))
        print("#################")
        cache = []
        j = 0
        my_socket.sendall(my_msg.encode())
        while j!=10:
            my_socket.sendall(my_msg_1.encode())
            server_bytes_msg_1 = my_socket.recv(1024)
            if len(server_bytes_msg_1) >100:
                print(server_bytes_msg_1,'63636363636363')
                cache.append(repr(server_bytes_msg_1))
                cache = cache[0].split("\\r\\n")
            print(cache,'@!@!@!@!@!')
            # print('Received:', repr(server_bytes_msg_1))
            j=j+1

        else:
            my_socket.close()
            return {"msg": "okay"}