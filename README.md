# pycm15 #

A lightweight Python interface to the CM15 X10 controller (a.k.a. CM15A).

Reads and writes X10 events and commands.  
Requires PyUSB library (0.x version).

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

## udev rule ##

In order to open the CM15 device without the need for root privileges,
create the file /etc/udev/rules.d/98-cm15a.rules and add:

    # X10 CM15a X10 controller
    ATTRS{idVendor}=="0bc7", ATTRS{idProduct}=="0001", MODE="664", GROUP="plugdev"
    
Then unplug and plug the CM15 again.
