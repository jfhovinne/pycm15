#!/usr/bin/python
"""
pycm15: a lightweight Python interface to the CM15 X10 controller
Reads and writes X10 events and commands
Requires PyUSB library (0.x version)
"""

import sys
import cm15

if len(sys.argv) != 4:
    print("This program sends a X10 command to the selected device")
    print("Usage: %s housecode device command" % sys.argv[0])
    print("Example: %s B 1 ON" % sys.argv[0])
    sys.exit(2)
else:
    cm15 = cm15.CM15()
    cm15.open()
    cm15.sendCommand(sys.argv[1], sys.argv[2], sys.argv[3])
    cm15.close()
