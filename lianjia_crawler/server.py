import contextlib
from collections.abc import Generator
import weakref
import aiohttp
from aiohttp import WSCloseCode, web


@contextlib.contextmanager
def websocket_graceful_shutdown(
    app: web.Application, ws: web.WebSocketResponse
) -> Generator[None, None, None]:
    app["websockets"].add(ws)
    try:
        yield
    finally:
        app["websockets"].discard(ws)


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    with websocket_graceful_shutdown(request.app, ws):
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


async def on_shutdown(app: web.Application) -> None:
    for ws in set(app["websockets"]):
        await ws.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")


async def make_app():
    app = web.Application()
    app["websockets"] = weakref.WeakSet()
    app.on_shutdown.append(on_shutdown)
    app.add_routes([web.get("/ws", websocket_handler)])
    return app


def main():
    web.run_app(make_app())
