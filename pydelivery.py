"""
PyDelivery

Re-imagining OSX AirDrop with Python

Author: Luke Mondy
"""
from __future__ import print_function
import sys, os
import time

from Tkinter import *

from zeroconf import ServiceBrowser, Zeroconf 
from zc_annoucers import ZConfAnnoucer, ZConfListener

from FileSender import FileSender
from FileReceiver import FileReceiver
from gui import MainGUI

from communication import DataReceiver, DataServer
import threading
import socket
import argparse
from sendfile import sendfile

def main():
	"""
	Main entry point
	"""

	# Parse any command-line args (I will add to these)
	parser = argparse.ArgumentParser()
	parser.add_argument("--test-as-listener", action = "store_true", default = True)
	parser.add_argument("--test-as-sender", action = "store_true", default = False)
	args = parser.parse_args()
	
	check_for_people_interval = 2000

	
	# Get to the main busines

	zconf = Zeroconf()
	try:
		# Bit of a hack to get local IP - see http://stackoverflow.com/a/166589/1728112
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8",80)) # Try connect to google DNS
		localip = (s.getsockname()[0])
		s.close()
	except Exception as e:
		sys.exit("Unable to determine your local IP address. Computer says:\n{}".format(e))
	
	# Step X - bind a port to listen on
	address = (localip,  0) # Let the OS choose a port
	dataserver = DataServer(address, DataReceiver)
	ip, port = dataserver.server_address

	dataserver_thread = threading.Thread(target=dataserver.serve_forever)
	dataserver_thread.daemon = True
	dataserver_thread.start()

	# Step X - annouce yourself on the network:
	hostname = socket.gethostname()
	properties = {"Nice name" : "Luke's VM"}
	zcannoucer = ZConfAnnoucer(zconf, "_http._tcp.", hostname,
			                 localip, port, properties = properties)

	# Step X - listen for anyone else annoucing:
	zclistener = ZConfListener()
	zcbrowser = ServiceBrowser(zconf, "_http._tcp.", zclistener)

	file_to_send = "test_file.zip"

	if args.test_as_sender:
		time.sleep(5)
		print("Peers!")
		for name, comm in zclistener.peers.iteritems():
			if hostname not in name: # Not localhost
				print("Trying to send file to {}:{}".format(comm.address, comm.port))
				sock = socket.socket()
				sock.connect((comm.address, comm.port))
				try:
					sock.sendall("receive file:{}".format(file_to_send))
					response = sock.recv(1024)
					print("Response from {}: {}".format(comm.address, response))
					if "OK" in response:
						print("got an OK")
						
						blocksize = os.path.getsize("test_file.zip")
						offset = 0
						with open("test_file.zip", 'r') as fb:
							while True:
								sent = sendfile(sock.fileno(), fb.fileno(), offset, blocksize)
								if sent == 0:
									break #EOF
								offset += sent

					else:
						print("Not OK to send")
				finally:
					sock.close()
		print("Done")
	else:
		# Step 3 - start up the GUI, and monitor the situation
		root=Tk()
		root.geometry("250x250+300+300")
		maingui = MainGUI(root)

		def task():
			if len(zclistener) > 0:
				for key, val in zclistener.peers.iteritems():
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
