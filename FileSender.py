import socket, os
from sendfile import sendfile

class FileSender():

	def __init__(self, filename, opensock):
		self.filename = filename
		self.opensock = opensock

		# Init and send!
		self.send()

		# This is a weird class..

	def send(self):
		print("sending {}".format(self.filename))
		blocksize = os.path.getsize(self.filename)
		offset = 0
		with open(self.filename, 'r') as fb:
			while True:
				sent = sendfile(self.opensock.fileno(), fb.fileno(), offset, blocksize)
				if sent == 0:
					break #EOF
				offset += sent
		print("sent!")
		return True


