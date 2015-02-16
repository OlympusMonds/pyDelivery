from __future__ import print_function
import threading
import SocketServer
import os

class DataReceiver(SocketServer.BaseRequestHandler):

    data = None
    filename = None

    def handle(self):

        print("\nPeers:\n{}\n".format("\n".join(self.server.peers.keys())))

        data = self.request.recv(1024)
        print("Received file offer:\n{}".format(data))
        self.filename = data.split(":")[-1]
        print("Filename: {}".format(self.filename))
        self.request.sendall("OK")

        # TODO
        # Maybe write to a temp file here, and then the finally
        # can move it over as needed.

        while True:
            data = self.request.recv(65536)
            if not data:
                break
            self.data = data

    def finish(self):
        # This is bad if the file is big, cause it will just 
        # sit in memory.
        print("Writing to file: {}".format(self.filename))

        if os.path.isfile(self.filename):
            print("File already exists. Overwrite?")
        with open("received_test_file.zip", 'w') as fb:
            fb.write(self.data)

	

class DataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=bind_and_activate)
        self.daemon_threads = True # this may or may not be useful

    def set_peers(self, peers):
        self.peers = peers

