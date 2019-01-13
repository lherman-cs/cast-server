from time import sleep
import asyncio
from threading import Thread
import json
from enum import IntEnum

import websockets

from cast import VideoPlayer


class Operation(IntEnum):
    AUTH = 0
    PLAY = 1
    PAUSE = 2
    STOP = 3
    NEXT = 4
    ADD = 5
    SEEK = 6


class Status(IntEnum):
    OK = 0


player = VideoPlayer()


async def auth_handler(req):
    return {
        "status": Status.OK
    }


async def play_handler(req):
    player.play()
    return {
        "status": Status.OK
    }


async def pause_handler(req):
    player.pause()
    return {
        "status": Status.OK
    }


async def stop_handler(req):
    player.stop()
    return {
        "status": Status.OK
    }


async def next_handler(req):
    player.next()
    return {
        "status": Status.OK
    }


async def add_handler(req):
    player.add(req["url"])
    return {
        "status": Status.OK
    }


async def seek_handler(req):
    player.seek(req["position"])
    return {
        "status": Status.OK
    }


handler_map = {
    Operation.AUTH: auth_handler,
    Operation.PLAY: play_handler,
    Operation.PAUSE: pause_handler,
    Operation.STOP: stop_handler,
    Operation.NEXT: next_handler,
    Operation.ADD: add_handler,
    Operation.SEEK: seek_handler
}


async def handler(websocket, path):
    is_auth = False
    while 1:
        message = await websocket.recv()
        req = json.loads(message)

        op = Operation(req['operation'])
        if op != Operation.AUTH and not is_auth:
            break

        resp = await handler_map[op](req)
        if op == Operation.AUTH:
            if Status(resp['status']) != Status.OK:
                break
            is_auth = True

        resp = json.dumps(resp)
        websocket.send(resp)


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websockets.serve(handler, port=8080))
    loop.run_forever()


if __name__ == '__main__':
    player_thread = Thread(target=player.main)
    server_thread = Thread(target=main)

    player_thread.start()
    server_thread.start()

    player_thread.join()
    server_thread.join()
