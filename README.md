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

To Do:
 - Automate annoucer details with local machine's IP, name, etc. Have good defaults that can be changed.
 - Figure out how to go from zeroconf info to actually transfering stuff.
    - Currently two machines can see each other with zeroconf. They can also send a file to one another using the FileSender and FileReceiver objects - HOWEVER, the file sending needs to be super explicit at the moment.
    - When a computer annouces on ZC, should it open a listening socket too? If so, should that socket be the file receiver object, or just a little socket to send info, like the filename, etc.? (probably the latter).
 - Refactor class names and stuff
 - I don't like how Tkinter is recording communicator objects. Buttons is fine, but there is no need for it have a list of communicators too! 
    - Should there be a Group object (that holds all the communicators?)
 - Keeping dead ZC communicators may be overkill... currently there is no recourse to waking them back up, and why would that be better? Just delete them!
 - Sooo much more.
