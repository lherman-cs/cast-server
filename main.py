from concurrent import futures
import time
import os
from queue import Queue

import grpc
import vscreen_pb2_grpc
from vscreen_pb2 import Status, StatusCode

from vscreen import VideoPlayer


class VScreenServicer(vscreen_pb2_grpc.VScreenServicer):
    def __init__(self, player: VideoPlayer):
        self.__player = player
        self.__player.add_subscriber(self)
        self.__subscribers_q = {}

    def Auth(self, request, context):
        # TODO! Actually do authentication
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Play(self, request, context):
        self.__player.play()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Pause(self, request, context):
        self.__player.pause()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Stop(self, request, context):
        self.__player.stop()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Next(self, request, context):
        self.__player.next()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Add(self, request, context):
        self.__player.add(request.url)
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Seek(self, request, context):
        self.__player.seek(request.value)
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Subscribe(self, request, context):
        queue = Queue()
        self.__subscribers_q[request.id] = queue

        while request.id in self.__subscribers_q:
            yield queue.get()

    def Unsubscribe(self, request, context):
        del self.__subscribers_q[request.id]
        response = Status(code=StatusCode.Value("OK"))
        return response

    def notify(self, data):
        for queue in self.__subscribers_q.values():
            queue.put(data)


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=os.cpu_count()))
player = VideoPlayer()
vscreen_servicer = VScreenServicer(player)
vscreen_pb2_grpc.add_VScreenServicer_to_server(vscreen_servicer, server)

# listen on port 8080
print('Starting server. Listening on port 8080.')
server.add_insecure_port('[::]:8080')
server.start()

player.main()
