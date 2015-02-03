"""
PyDelivery

Re-imagining OSX AirDrop with Python

Author: Luke Mondy
"""
import sys
from listener import Listener
from zeroconf import ServiceBrowser, Zeroconf, raw_input

def main():
	"""
	Main entry point
	"""
	zeroconf = Zeroconf()
	listen = Listener()
	browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listen)

	try:
		raw_input("Press enter to exit")
	finally:
		zeroconf.close()

if __name__ == "__main__":
	sys.exit(main())

