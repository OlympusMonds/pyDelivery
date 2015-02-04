"""
Listener object

"""
from __future__ import print_function
from Communicator import Communicator

class Listener():

	def __init__(self):
		self.communicators = {}

	def add_service(self, zeroconf, type, name):
		info = zeroconf.get_service_info(type, name)
		self.communicators[name] = Communicator(name, info)
		print("Service {} added".format(name))

	def remove_service(self, zeroconf, type, name):
		self.communicators[name].kill()
		print("Service {} is removed".format(name))

	@property
	def communicators(self):
		return self.communicators

	@property
	def alive_communicators(self):
		return {key: val for key, val in self.communicators.iteritems() if val.alive}

	def __len__(self):
		return len(self.communicators.keys())
