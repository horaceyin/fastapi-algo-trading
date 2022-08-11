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

@live_trading_router.post('/subscribe-ticker-price', status_code=status.HTTP_200_OK) # To get ticker price of futures # need session token and product code0
async def get_ticker_price(request: GetTickerPriceModel):
    userId = request.userId
    spServerKey = request.spServerKey
    sessionTime = request.sessionTime

    my_msg = f'4104,0,{userId},{spServerKey},3,8.7,1.0,1.0,SP_F,{sessionTime},0\r\n' # Do not need ticker price 
    my_msg_1 = f'4107,0,HSIQ1,0,1,2,\r\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((SP_PRICE_SERVER_HOST, SP_PRICE_SERVER_PORT))
        
        print("#################")
        my_socket.sendall(my_msg.encode())
        try:
            while True:
                my_socket.sendall(my_msg_1.encode())
                server_bytes_msg_1 = my_socket.recv(1024)
                print('Received:', repr(server_bytes_msg_1))
                print('***************')
                # Received: b'4107,3,-1,HSIQ1,1,2\r\n'
                # ***************
        except KeyboardInterrupt:
            my_socket.close()
            return {"msg": "okay"}