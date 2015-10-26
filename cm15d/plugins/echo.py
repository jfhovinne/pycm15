from yapsy.IPlugin import IPlugin
from pprint import pprint

class Echo(IPlugin):
    def cm15DataReceivedHandler(self, data):
        print("Data received: ")
        pprint(data)
    def cm15DataWrittenHandler(self, data):
        print("Data written: ")
        pprint(data)
