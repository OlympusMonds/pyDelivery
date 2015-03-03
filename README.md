# PyDelivery
A program to share files easily over a local network. May have some similarities to Apple AirDrop.


Dependencies:
 - zeroconf  : pip install zeroconf
 - six       : pip install six
 - pysendfile: pip install pysendfile
 - cython    : pip install cython
 - kivy      : pip install kivy
   - Kivy seems to have a bug with particular versions of libc, which is pretty major. I've had issues with Linux Mint 16 and Debian 6 in regard to this issue. Upgrading to Debian 7 fixed it for me :s

To Do:
  - Figure out how the SockerServer handle function can either pass its data out, or some other function pass something in, so it can save the right filename, etc.
 - Get some safties in there. If a transfer fails, catch the exception, delete the file, etc.
   - Actually, look into Twisted
     - Twisted looks painful...
