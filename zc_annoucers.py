"""
Holds the classes used for ZeroConf annouces: both the server and listener
"""

from zeroconf import ServiceInfo, ServiceBrowser
import socket
from peer import Peer

class ZConfAnnoucer():

    def __init__(self, zconf, type, name, address, port, weight=0, priority=0, properties=None):
	self.zconf = zconf
	self.info = ServiceInfo(type, "{}.{}".format(name, type),
					    socket.inet_aton(address), int(port),
					    weight, priority, properties)
	self.zconf.register_service(self.info)


    def remove_service(self, zconf):
	zconf.unregister_service(self.info)



class ZConfListener():

    def __init__(self, localip):
	self.peers = {}
	self.localip = localip


    def add_service(self, zconf, type, name):
	info = zconf.get_service_info(type, name)
	if socket.inet_ntoa(info.address) != self.localip:
	    # Don't add yourself to the list of peers
	    self.peers[name] = Peer(name, info)
	    print("Service {} added".format(name))


    def remove_service(self, zconf, type, name):
	del self.peers[name]
	print("Removed {} service".format(name))


    @property
    def peers(self):
	return self.peers

    def __len__(self):
	return len(self.peers.keys())
