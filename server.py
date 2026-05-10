import aiohttp
from aiohttp import web


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == "close":
                await ws.close()
            else:
                await ws.send_str(msg.data + "/answer")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ws connection closed with exception %s" % ws.exception())

    print("websocket connection closed")

    return ws


async def make_app():
    app = web.Application()
    app.add_routes([web.get("/ws", websocket_handler)])
    return app


web.run_app(make_app())
