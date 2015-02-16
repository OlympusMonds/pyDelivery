# pyDelivery
Apple AirDrop, reimagined in Python.

This is what AirDrop is: http://support.apple.com/en-au/HT203106

It is very useful, except it is limited to OSX and other Apple stuff. My goal is to implement a similar system in Python, so we can all use it!


Dependencies:
 - zeroconf  : pip install zeroconf
 - six       : pip install six
 - pysendfile: pip install pysendfile

To Do:
 - Move from TKinter to Kivy (if it's OK). This may open the door to deploying on Android/iOS/Windows more easily.
 - Figure out how the SockerServer handle function can either pass its data out, or some other function pass something in, so it can save the right filename, etc.
   - Need to subclass the server, to make a constructer with (perhaps) a pointer to the Peer in question. Then the handle function can access it OK. See here: http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python
 - Get some safties in there. If a transfer fails, catch the exception, delete the file, etc.
   - Actually, look into Twisted. 
