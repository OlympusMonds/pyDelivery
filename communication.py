from __future__ import print_function
import threading
import SocketServer
from FileReceiver import FileReceiver


class DataReceiver(SocketServer.BaseRequestHandler):

	def handle(self):
		data = self.request.recv(1024)
		print("Received file offer:\n{}".format(data))
		filename = data.split(":")[0]
		print("Filename: {}".format(filename))
		print(self.request)
		#fr = FileReceiver(filename, , 8889)
		self.request.sendall("OK")


	

class DataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


