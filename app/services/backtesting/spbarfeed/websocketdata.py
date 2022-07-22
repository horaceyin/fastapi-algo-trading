import websockets
import asyncio
HOST = 'futures.spsystem.info'      
addr = 'ws://'+ HOST +':9032'
st = '4104,0,SPANSONLI,B0D84F1C83169555E014213EE24E98FA,3,8.7,1.0,1.0,SP_F,1658303534,0'
st2 = '4107,0,HSIN2,0,1,0'
async def data(url):
    with websockets.connect(url) as websocket:
        try:
            await websocket.send(st)
            res = await websocket.recv()
            print(res)
            await websocket.send(st2)
            res1 = await websocket.recv()
            print(res1)
        finally:
            await websocket.close()
asyncio.get_event_loop().run_until_complete(data(addr))
# asyncio.get_event_loop().run_forever()
