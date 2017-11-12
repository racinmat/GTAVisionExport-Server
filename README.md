# This is socket client for GTAVisionExport
GTAVisionExport managed plugin has socket server on port 5555.
This is webserver + socket client which enables to instruct the managed plugin.

## Installation
Install all needed libraries by `pip install -r requirements.txt`

## Starting
Simply start the server nd socket client by `python main.py`

Make sure you start it after your GTA V is running!

## Accessing it from other devices
If using WAMP server, just copy `index.html` to some place in `www` directory.
Then, if you can not access it from other device in local site (`192.168.0.*` address)
Modify both `httpd.conf` and `httpd-vhosts.conf`
and put `Require ip 192.168.0` right after the `Require local` line, wherever it is.