#!/usr/bin/python
"""
pycm15: a lightweight Python interface to the CM15 X10 controller
Reads and writes X10 events and commands
Requires PyUSB library (0.x version)
"""

import sys
import threading
import usb
import time
from .x10 import X10
from pprint import pprint

class CM15():
    def __init__(self):
        self.VENDOR_ID = 0x0BC7
        self.PRODUCT_ID = 0x0001
        self.WRITE_ENDPOINT = 0x02
        self.READ_ENDPOINT = 0x81
        self.DATA_SIZE = 8
        
        self.device = None
        self.eventHandlers = {'foundDevice': [], 'dataReceived': [], 'dataWritten': []}

    def open(self):
        busses = usb.busses()

        for bus in busses:
            for dev in bus.devices:
                if dev.idVendor == self.VENDOR_ID and dev.idProduct == self.PRODUCT_ID:
                    self.device = dev
                    for eventHandler in self.eventHandlers['foundDevice']:
                        eventHandler(self.device)

        if self.device is None:
            sys.exit("Could not find CM15 device.")
            
        self.getDeviceHandle()

    def getDeviceHandle(self):
        self.deviceHandle = self.device.open()
        self.deviceHandle.setConfiguration(1)
        self.deviceHandle.claimInterface(0)
        return(self.deviceHandle)
        
    def close(self):
        self.deviceHandle.releaseInterface()
        
    def startListening(self):
        self.listening = True
        thread = threading.Thread(target = self.read)
        thread.start()
    
    def stopListening(self):
        self.listening = False
        
    def subscribeToEvent(self, eventName, eventHandler):
        self.eventHandlers[eventName].append(eventHandler)
        
    def unsubscribeToEvent(self, eventName, eventHandler):
        self.eventHandlers[eventName].remove(eventHandler)
    
    def read(self):
        while self.listening:
            try:
                data = self.deviceHandle.bulkRead(self.READ_ENDPOINT, self.DATA_SIZE, 1000)
                for eventHandler in self.eventHandlers['dataReceived']:
                    eventHandler(data)
            except usb.USBError:
                pass

    def bulkWrite(self, data):
        try:
            self.deviceHandle.bulkWrite(self.WRITE_ENDPOINT, data, 1000)
            for eventHandler in self.eventHandlers['dataWritten']:
                eventHandler(data)
        except usb.USBError:
            pass

    def sendCommand(self, code, command):
        if len(code) == 1:
            comm = X10.encodeCommand(code, command)
            self.bulkWrite([0x06, comm])
        elif len(code) < 4:
            addr = X10.encodeAddress(code, True)
            comm = X10.encodeCommand(code[0], command)
            self.bulkWrite([0x04, addr])
            time.sleep(1)
            self.bulkWrite([0x06, comm])
        else:
            pass

