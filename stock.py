import asyncio

import websockets


async def hello():
    uri = 'ws://stream240.forexpros.com/echo/314/5f0duoyc/websocket:8080'
    async with websocket.connect(uri) as websocket:
        data = [
            "{\"_event\":\"bulk-subscribe\",\"tzID\":28,\"message\":\"pid-40820:%%pid-942630:%%pid-28930:%%pid-954522:%%pid-179:%%pid-169:%%pid-166:%%pid-14958:%%pid-170:%%pid-44336:%%pid-24441:%%pid-17920:%%pid-27254:%%pid-172:%%pid-27:%%pid-167:%%pid-175:%%pid-168:%%pid-174:%%pid-177:%%pid-176:%%pid-14600:%%pid-14601:%%pid-1016254:%%pid-25685:%%pid-13666:%%pid-13665:%%pid-14602:%%pid-38014:%%pid-19155:%%pid-10529:%%pid-11319:%%pid-178:%%pid-171:%%pid-38017:%%pid-38015:%%pid-37426:%%pid-29049:%%pid-17940:%%pid-39929:%%pid-995072:%%pid-29151:%%pid-8873:%%pid-8839:%%pid-8827:%%pid-1:%%pid-2:%%pid-3:%%pid-5:%%pid-7:%%pid-9:%%pid-10:%%pidTechSumm-1:%%pidTechSumm-2:%%pidTechSumm-3:%%pidTechSumm-5:%%pidTechSumm-7:%%pidTechSumm-9:%%pidTechSumm-10:%%isOpenExch-54:%%isOpenExch-21:%%isOpenExch-20:%%isOpenPair-8873:%%isOpenPair-8839:%%isOpenPair-8827:%%domain-6:\"}"
        ]
        await websockets.send(data)
        await websocket.recv()


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
