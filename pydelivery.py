"""
PyDelivery

Re-imagining OSX AirDrop with Python

Author: Luke Mondy
"""
from __future__ import print_function
import sys
import time

from Tkinter import *
from zeroconf import ServiceBrowser, Zeroconf 
from Listener import Listener
from Server import Server
from FileSender import FileSender
from FileReceiver import FileReceiver
from gui import MainGUI

from communication import DataReceiver, DataServer
import threading
import socket


def main():
	"""
	Main entry point
	"""
	check_for_people_interval = 2000

	zconf = Zeroconf()
	try:
		# Bit of a hack to get local IP - see http://stackoverflow.com/a/166589/1728112
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8",80)) # Try connect to google DNS
		localip = (s.getsockname()[0])
		s.close()
	except:
		sys.exit("Unable to determine your local IP address.")
	
	# Step X - bind a port to listen on
	address = (localip,  0) # Let the OS choose a port
	dataserver = DataServer(address, DataReceiver)
	ip, port = dataserver.server_address

	print(ip, port)

	dataserver_thread = threading.Thread(target=dataserver.serve_forever)
	dataserver_thread.daemon = True
	dataserver_thread.start()

	# Step X - annouce yourself on the network:
	hostname = socket.gethostname()
	properties = {"Nice name" : "Luke's VM"}
	annoucer = Server(zconf, "_http._tcp.", hostname,
			  localip, port, properties = properties)

	# Step X - listen for anyone else annoucing:
	listen = Listener()
	browser = ServiceBrowser(zconf, "_http._tcp.", listen)
	


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

if __name__ == "__main__":
	sys.exit(main())


	#fr = FileReceiver("received_test_file.zip", "127.0.0.1", 8889)
	#fr.receive()
	#fs = FileSender("test_file.zip", "127.0.0.1", 8889)
	#fs.send()
