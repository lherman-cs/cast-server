from concurrent import futures
import grpc
import time
import os

from vscreen import VideoPlayer

import vscreen_pb2_grpc
from vscreen_pb2 import Status, StatusCode

player = VideoPlayer()


class VScreenServicer(vscreen_pb2_grpc.VScreenServicer):
    def Auth(self, request, context):
        # TODO! Actually do authentication
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Play(self, request, context):
        player.play()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Pause(self, request, context):
        player.pause()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Stop(self, request, context):
        player.stop()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Next(self, request, context):
        player.next()
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Add(self, request, context):
        player.add(request.url)
        response = Status(code=StatusCode.Value("OK"))
        return response

    def Seek(self, request, context):
        player.seek(request.value)
        response = Status(code=StatusCode.Value("OK"))
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=os.cpu_count()))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
vscreen_pb2_grpc.add_VScreenServicer_to_server(VScreenServicer(), server)

# listen on port 8080
print('Starting server. Listening on port 8080.')
server.add_insecure_port('[::]:8080')
server.start()

player.main()
