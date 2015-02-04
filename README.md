# pyDelivery
Apple AirDrop, reimagined in Python.

This is what AirDrop is: http://support.apple.com/en-au/HT203106

It is very useful, except it is limited to OSX and other Apple stuff. My goal is to implement a similar system in Python, so we can all use it!

The current plan is this:
 - Use zeroconf to allow two machines running PyDelivery to see each other, and setup a transfer.
 - Use TKinter to show this in a visually appealing way (tk may not be built for looking good...)
 - Investigate setting up a new WiFi network with Python
    - This may be impossible.

Dependencies:
 - zeroconf: pip install zeroconf
 - six     : pip install six
