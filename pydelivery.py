"""
PyDelivery

Re-imagining OSX AirDrop with Python

Author: Luke Mondy
"""
from __future__ import print_function
import sys
import time

from Listener import Listener
from Server import Server
from FileSender import FileSender
from FileReceiver import FileReceiver
from zeroconf import ServiceBrowser, Zeroconf, raw_input

def main():
	"""
	Main entry point
	"""
	zeroconf = Zeroconf()

	listen = Listener()
	browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listen)
	
	fr = FileReceiver("received_test_file.zip", "127.0.0.1", 8889)
	fr.receive()
	fs = FileSender("test_file.zip", "127.0.0.1", 8889)
	fs.send()

	count = 0
	while listen.number_of_servers() == 0:
		count += 1

		if count == 10:
			desc = {"Filename": "thing_to_send.zip",
				"Sender":   "Luke"}
			serve = Server(zeroconf, "_http._tcp.local.", "Luke's computer", 
				       "127.0.0.1", 8888, properties=desc)
		print(count)
		time.sleep(1)
	
	print(browser)
	print("Done")

	try:
		raw_input("Press enter to exit")
	finally:
		zeroconf.close()

if __name__ == "__main__":
	sys.exit(main())

