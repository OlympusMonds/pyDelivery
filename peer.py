"""
Peer class

A peer is another person just like you. They can send and receive files,
and annouce themselves onto the network.
"""

import socket

class Peer():
	
	def __init__(self, name, info):
		self.name = name
		self.address = socket.inet_ntoa(info.address)
		self.port = info.port

		self.info = info

	def __repr__(self):
		return "{name} @ {address}:{port}".format(name = self.name,
			   			                          address = self.address,
							                      port = self.port)

	def __str__(self):
		return self.__repr__()
