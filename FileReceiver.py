import socket, os

class FileReceiver():

	def __init__(self, filename, host, port):
		self.filename = filename 
		self.host = host
		self.port = port
		pass

	def receive(self):
		sock = socket.socket()
		sock.bind((self.host, self.port))
		sock.listen(1)

		while True:
			asock, address = sock.accept()

			with open(self.filename, 'w') as fb:
				while True:
					data = asock.recv(65536)
					if not data:
						break
					fb.write(data)
			asock.close()
		sock.close()



