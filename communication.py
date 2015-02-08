from __future__ import print_function
import threading
import SocketServer

class DataReceiver(SocketServer.BaseRequestHandler):

	def handle(self):
		data = self.request.recv(1024)
		cur_thread = threading.currentThread()
		print("Thread {thread} received:\n{data}".format(thread=cur_thread, data=data))

	

class DataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass


