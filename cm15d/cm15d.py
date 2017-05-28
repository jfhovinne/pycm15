#! /usr/bin/env python

from ConfigParser import SafeConfigParser
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
        # A command has been received, e.g. "B1 ON". Execute it.
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
    def __init__(self, plugins):
        self.plugins = plugins

    def buildProtocol(self, addr):
        return CM15Daemon(self)

    def startFactory(self):
        # Open the CM15 interface in startFactory so we can close it in stopFactory
        self.cm15 = cm15.CM15()
        self.cm15.open()

        # Activate plugins event handlers
        for plugin in self.plugins.getAllPlugins():
            if plugin.is_activated:
                self.cm15.subscribeToEvent('dataReceived', plugin.plugin_object.cm15DataReceivedHandler)
                self.cm15.subscribeToEvent('dataWritten', plugin.plugin_object.cm15DataWrittenHandler)

        # Listen for CM15 events
        self.cm15.startListening()

    def stopFactory(self):
        self.cm15.stopListening()
        self.cm15.close()


def main():
    # Read configuration
    config = SafeConfigParser(
        defaults = {'port':'15915',
                    'plugins_directory':'./plugins',
                    'plugins_enabled':'',
                   })
    config.read(['./conf/cm15d.conf',
                 '/etc/cm15d.conf',
                 '/etc/cm15d/cm15d.conf',
                 '/etc/cm15d/conf.d/local.conf',
                ])

    # Activate enabled plugins
    plugins = PluginManager()
    plugins.setPluginPlaces(config.get('cm15d', 'plugins_directory').split(','))
    plugins.collectPlugins()
    plugins_enabled = config.get('cm15d', 'plugins_enabled').split(',')

    for plugin in plugins.getAllPlugins():
        if plugin.name in plugins_enabled:
            plugins.activatePluginByName(plugin.name)
            print("Plugin %s enabled" % plugin.name)

    # Start server
    port = int(config.get('cm15d', 'port'))
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(CM15DaemonFactory(plugins))
    print("Server listening on port %s" % port)
    reactor.run()

if __name__ == '__main__':
    main()
