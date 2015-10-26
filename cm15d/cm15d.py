#! /usr/bin/env python

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from yapsy.PluginManager import PluginManager
import sys
import cm15

class CM15Daemon(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        args = data.replace('\n', '').replace('\r', '').split(' ')
        if len(args) == 2:
            try:
                self.factory.cm15.sendCommand(args[0], args[1])
                self.transport.write("OK\n")
            except ValueError:
                self.transport.write("SYNTAX ERROR\n")
            except:
                self.transport.write("ERROR\n")
        else:
            self.transport.write("SYNTAX ERROR\n")

class CM15DaemonFactory(Factory):
    def buildProtocol(self, addr):
        return CM15Daemon(self)

    def startFactory(self):
        self.loadPlugins()
        self.cm15 = cm15.CM15()
        self.cm15.open()
        for plugin in self.pluginManager.getAllPlugins():
            self.cm15.subscribeToEvent('dataReceived', plugin.plugin_object.cm15DataReceivedHandler)
            self.cm15.subscribeToEvent('dataWritten', plugin.plugin_object.cm15DataWrittenHandler)
        self.cm15.startListening()

    def stopFactory(self):
        self.cm15.stopListening()
        self.cm15.close()

    def loadPlugins(self):
        self.pluginManager = PluginManager()
        self.pluginManager.setPluginPlaces(["./plugins"])
        self.pluginManager.collectPlugins()
        for plugin in self.pluginManager.getAllPlugins():
            self.pluginManager.activatePluginByName(plugin.name)

endpoint = TCP4ServerEndpoint(reactor, int(sys.argv[1]))
endpoint.listen(CM15DaemonFactory())
reactor.run()
