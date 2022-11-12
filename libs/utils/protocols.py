from kivy.support import install_twisted_reactor
install_twisted_reactor()
import json

from autobahn.twisted.websocket import WebSocketClientProtocol, \
                                       WebSocketClientFactory


class MyKivyClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.factory._app.print_message('WebSocket connection open.')
        self.factory._proto = self
        self.send({
            'pk': "3",
            'action': "start_listen",
            'request_id': 123,
        })
    
    def send(self, message):
        if self.factory._proto:
            self.sendMessage(json.dumps(message).encode('utf-8'))
            print("sended")
        else:
            print("can't send")

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.factory._app.print_message("Binary message received: {0} bytes".format(len(payload)))
        else:
            self.factory._app.print_message("Got from server: {}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        self.factory._app.print_message("WebSocket connection closed: {0}".format(reason))
        self.factory._proto = None


class MyKivyClientFactory(WebSocketClientFactory):
    protocol = MyKivyClientProtocol

    def __init__(self, url, app):
        WebSocketClientFactory.__init__(self, url)
        # While the Kivy app needs a reference to the factory,
        # the factory needs a reference to the Kivy app.
        self._app = app
        # Not sure why/whether _proto is needed?
        self._proto = None
