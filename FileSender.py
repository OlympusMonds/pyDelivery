import socket, os
from sendfile import sendfile

class FileSender():

	def __init__(self, filename, destination, port):
		self.filename = filename
		self.destination = destination
		self.port = port


	def send(self):
		print("sending")
		print(self.destination, self.port)
		blocksize = os.path.getsize(self.filename)
		offset = 0
		with open(self.filename, 'r') as fb:
			sock = socket.socket()
			sock.connect((self.destination, self.port))

			while True:
				sent = sendfile(sock.fileno(), fb.fileno(), offset, blocksize)
				if sent == 0:
					break #EOF
				offset += sent
		print("sent!")
		return True


