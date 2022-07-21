import websockets
import asyncio
 
addr = 'ws://futures.spsystem.info:9032'
st = '4104,0,SPANSONLI,B0D84F1C83169555E014213EE24E98FA,3,8.7,1.0,1.0,SP_F,1658306145,0'
st2 = '4107,0,HSIN2,0,1,0'
async def data(url):
    websockets.connect(url)
    await websockets.send(st)
    res = await websockets.recv()
    print(res)
    await websockets.send(st2)
    res1 = await websockets.recv()
    print(res1)
asyncio.get_event_loop().run_until_complete(data(addr))
asyncio.get_event_loop().run_forever()

