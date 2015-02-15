from __future__ import print_function
import threading
import SocketServer
from FileReceiver import FileReceiver


class DataReceiver(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        print("Received file offer:\n{}".format(data))
        filename = data.split(":")[-1]
        print("Filename: {}".format(filename))
        self.request.sendall("OK")

        with open("received_test_file.zip", 'w') as fb:
            while True:
                data = self.request.recv(65536)
                if not data:
                    break
                fb.write(data)


	

class DataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


