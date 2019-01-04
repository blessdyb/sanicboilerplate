import asyncio
import uvloop
from signal import signal, SIGINT
from src import app


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    server = app.run(host='0.0.0.0', port=8080)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    signal(SIGINT, lambda s, f: loop.stop())
    try:
        loop.run_forever()
    except:
        loop.stop()
