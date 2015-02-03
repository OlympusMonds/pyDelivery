"""
Listener object

"""
from __future__ import print_function
from zeroconf import ServiceBrowser, Zeroconf, raw_input

class Listener():
	
	def add_service(self, zeroconf, type, name):
		info = zeroconf.get_service_info(type, name)
		print("Service {} added, service info: {}".format(name, info))

	def remove_service(self, zeroconf, type, name):
		print("Service {} is removed".format(name))


