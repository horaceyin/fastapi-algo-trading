import websockets
import asyncio
import time
 
addr = 'ws://futures.spsystem.info:9032'
st = '4104,0,SPANSONLI,B0D84F1C83169555E014213EE24E98FA,3,8.7,1.0,1.0,SP_F,1658306145,0\r\n'
st2 = '4107,0,HSIN2,0,1,0\r\n'
# async def data():
#     addr = 'ws://futures.spsystem.info:9032'
#     st = '4104,0,SPANSONLI,B0D84F1C83169555E014213EE24E98FA,3,8.7,1.0,1.0,SP_F,1658306145,0\r\n'
#     st2 = '4107,0,HSIN2,0,1,0\r\n'
#     async with websockets.connect(addr) as websocket:
#         print('@@@@')
#         websocket.send(st)
#         res = await websocket.recv()
#         print(res)
#         await websocket.send(st2)
#         while True:
#             res1 = await websocket.recv()
#             print(res1)
#             print('***********************')
# asyncio.run(data())


# asyncio.run(data())
# async def data():
#     async with websockets.connect('ws://futures.spsystem.info:9032') as websocket:
#         await websocket.send(st)
#         res = await websocket.recv()
#         return res
#     await websockets.send(st2)
#     print('Msg2 sent')
#     while True:
#         try:
#             res = await websockets.recv()
#             print(res)
#         except KeyboardInterrupt:
#             False
# loop = asyncio.get_event_loop()
# data = data()
# result = loop.run_until_complete(data)
# print(result)
# loop.close()
