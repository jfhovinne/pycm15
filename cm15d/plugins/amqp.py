from yapsy.IPlugin import IPlugin
import pika

class AMQP(IPlugin):
    def cm15DataReceivedHandler(self, data):
        self.sendData('CM15DataReceived', data)

    def cm15DataWrittenHandler(self, data):
        self.sendData('CM15DataWritten', data)

    def sendData(self, queue, data):
        out = ' '.join(str(v) for v in data) + '\n'
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='', routing_key=queue, body=out)
        connection.close()
