from time import sleep
import asyncio
from threading import Thread
import json
from enum import Enum

import websockets

from cast import VideoPlayer


class Operation(Enum):
    AUTH = 0
    PLAY = 1
    PAUSE = 2
    NEXT = 3
    ADD = 4
    SEEK = 5


class Status(Enum):
    OK = 0


player = VideoPlayer()


async def auth_handler(req):
    print("auth")
    return {
        "status": 0
    }


async def play_handler(req):
    print("play")
    player.play()
    return {
        "status": 0
    }


async def pause_handler(req):
    print(pause)
    player.pause()
    return {
        "status": 0
    }


async def next_handler(req):
    player.next()
    return {
        "status": 0
    }


async def add_handler(req):
    print('add')
    player.add(req["url"])
    return {
        "status": 0
    }


async def seek_handler(req):
    player.seek(req["position"])
    return {
        "status": 0
    }


handler_map = {
    Operation.AUTH: auth_handler,
    Operation.PLAY: play_handler,
    Operation.PAUSE: pause_handler,
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
