"""
PyDelivery

Server class
"""

from zeroconf import ServiceInfo, ServiceBrowser, Zeroconf, raw_input
import socket

class Server():

	def __init__(self, zconf, type, name, address, port, weight=0, priority=0, properties=None):
		"""
		Initialise the server with a service
		and register it.
		"""
		self.zconf = zconf
		print(properties)
		self.info = ServiceInfo(type,
					"{}.{}".format(name,type),
					socket.inet_aton(address),
					int(port),
					weight,
					priority,
					properties)
		self.zconf.register_service(self.info)

	def remove_service(self, zconf):
		zconf.unregister_service(self.info)


