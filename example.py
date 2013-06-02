#!/usr/bin/python
"""
pycm15: a lightweight Python interface to the CM15 X10 controller
Reads and writes X10 events and commands
Requires PyUSB library (0.x version)
"""

import time
from pprint import pprint
import cm15

# Triggered when the CM15 listens and receives raw data
def dataReceivedHandler(data):
    print("Data received: ")
    pprint(data);

# Prepare interface and register event handler
cm15 = cm15.CM15()
cm15.subscribeToEvent('dataReceived', dataReceivedHandler)

# Open device, start listening for events and wait 5 seconds
cm15.open()
cm15.startListening()
time.sleep(5)

# Stop listening and close device
cm15.stopListening()
cm15.close()
