"""
PyDelivery

Re-imagining OSX AirDrop with Python

Author: Luke Mondy
"""
from __future__ import print_function
import sys
import time

from Tkinter import *
from zeroconf import ServiceBrowser, Zeroconf, raw_input

from Listener import Listener
from Server import Server
from FileSender import FileSender
from FileReceiver import FileReceiver
from gui import MainGUI

def main():
	"""
	Main entry point
	"""
	check_for_people_interval = 2000

	zeroconf = Zeroconf()

	# Step 1 - annouce yourself on the network:
	properties = {"Nice name" : "Luke's VM"}
	annoucer = Server(zeroconf, "_http._tcp.", "Luke's VM",
			  "192.168.1.11", 8888, properties = properties)

	# Step 2 - listen for anyone else annoucing:
	listen = Listener()
	browser = ServiceBrowser(zeroconf, "_http._tcp.", listen)

	# Step 3 - start up the GUI, and monitor the situation
	root=Tk()
	root.geometry("250x250+300+300")
	maingui = MainGUI(root)

	def task():
		if len(listen) > 0:
			for key, val in listen.alive_communicators.iteritems():
				maingui.add_communicator(val)
		root.after(check_for_people_interval, task)  # reschedule event in 1 seconds

	root.after(check_for_people_interval, task)
	root.mainloop()
	"""	
	try:
		raw_input("Press enter to exit")
	finally:
		zeroconf.close()
	"""

if __name__ == "__main__":
	sys.exit(main())


	#fr = FileReceiver("received_test_file.zip", "127.0.0.1", 8889)
	#fr.receive()
	#fs = FileSender("test_file.zip", "127.0.0.1", 8889)
	#fs.send()
