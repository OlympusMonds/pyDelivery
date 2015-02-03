"""
Listener object

"""
from __future__ import print_function, unicode_literals
from zeroconf import ServiceBrowser, Zeroconf, raw_input
import socket

class Listener():

	def __init__(self):
		self.servers = {}

	def add_service(self, zeroconf, type, name):
		info = zeroconf.get_service_info(type, name)
		self.servers[name] = info
		print("Service {} added".format(name))
		print("Type is {}".format(type))
		if info:
			print("  Address is {}:{}".format(socket.inet_ntoa(info.address),
							  info.port))
			print("  Weight is {}, Priority is {}".format(info.weight,
								      info.priority))
			print("  Server is {}".format(info.server))

			if info.properties:
				print("  Properties are")
				for key, value in info.properties.items():
					print("    {}: {}".format(key, value))
		else:
			print("  No info")
		print("\n")

	def remove_service(self, zeroconf, type, name):
		print("Service {} is removed".format(name))

	def number_of_servers(self):
		return len(self.servers.keys())
