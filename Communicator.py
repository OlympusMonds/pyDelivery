"""
This class is for "people". When you find a computer who is broadcasting
make a communicator to hold all the info
"""

import socket

class Communicator():

	def __init__(self, name, info):
		self.name = name
		self.address = socket.inet_ntoa(info.address)
		self.port = info.port

		self.info = info

		self.alive = True


	def kill(self):
		self.alive = False

	def __repr__(self):
		health = "ALIVE" if self.alive else "DEAD "
		return "{health} - {name} @ {address}:{port}".format(name = self.name,
				   	   			     address = self.address,
							             port = self.port,
								     health = health)
	def __str__(self):
		return self.__repr__()

	
