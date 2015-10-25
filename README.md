# pycm15 #

A lightweight Python interface to the CM15 X10 controller (a.k.a. CM15A).

Reads and writes X10 events and commands.
Requires PyUSB library (0.x version).
Tested on Debian Wheezy.

## Usage example ##

    import cm15

    # Prepare interface
    cm15 = cm15.CM15()
    # Open device
    cm15.open()
    # Start listening for events
    cm15.startListening()
    # Stop listening
    cm15.stopListening()
    # Close device
    cm15.close()
    
### Event handlers ###

    import time
    from pprint import pprint
    import cm15

    # Triggered when the CM15 listens and receives raw data
    def dataReceivedHandler(data):
        print("Data received: ")
        pprint(data)

    # Prepare interface and register event handler
    cm15 = cm15.CM15()
    cm15.subscribeToEvent('dataReceived', dataReceivedHandler)

    # Open device, start listening for events and wait 5 seconds
    cm15.open()
    cm15.startListening()
    time.sleep(5)

    # If the CM15 receives data, it will be printed on the screen 

    # Stop listening and close device
    cm15.stopListening()
    cm15.close()

### Sending X10 commands ###

    # Send X10 commands: B1 ON, B1 OFF
    print("Select device B1")
    cm15.bulkWrite([0x04, 0xE6])
    # A minimal delay is required between commands
    time.sleep(1)
    print("Send B ON")
    cm15.bulkWrite([0x06, 0xE2])
    time.sleep(5)
    print("Select device B1")
    cm15.bulkWrite([0x04, 0xE6])
    time.sleep(1)
    print("Send B OFF")
    cm15.bulkWrite([0x06, 0xE3])

## Sending X10 commands using cm15send.py ##

Usage: python cm15send.py code command

Send B ON

    python cm15send.py B ON

Send B1 OFF

    python cm15send.py B1 OFF

## udev rule ##

In order to open the CM15 device without the need for root privileges,
create the file /etc/udev/rules.d/98-cm15a.rules and add:

    # X10 CM15a X10 controller
    ATTRS{idVendor}=="0bc7", ATTRS{idProduct}=="0001", MODE="664", GROUP="plugdev"
    
Then unplug and plug the CM15 again.

## CM15d server ##

A TCP server based on Python Twisted (12.0+) is available in cm15d/cm15d.py.
This TCP server listens for incoming X10 commands and sends them to the controller.
It also listens for X10 events received by the controller (e.g. from RF sensors).
These events are not handled yet (see cm15DataReceivedHandler).

The user executing the cm15d process needs to be part of the plugdev group,
as explained above.

Usage: python cm15d.py port

    python cm15d.py 15915

Python Twisted (12.0+) must be installed for this to work of course.

For the client, use e.g. Netcat.

Send B1 ON

    nc localhost 15915
    B1 ON(Enter)

Quit with CTRL+C.

One-liner

    echo B1 ON | nc -q1 localhost 15915

You can daemonize cm15d with Supervisor (since twistd implementation is not available yet).

First, ensure Supervisor is installed, then create the configuration file for cm15d:

    [program:cm15d]
    command=/path/to/cm15d.py 15915
    user=cm15user

Remember: cm15user needs to be part of the plugdev group.
