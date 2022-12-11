from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import logging
import json
from libs.models import createMessage, createUser

from settings import Logger

name = __name__

class AppWebsocketClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        Logger.info(f"{name}: Websocket connection opened")
        self.send({
            'pk': "3",
            'action': "start_listen",
            'request_id': 123,
        })
    
    def send(self, message):
        if self:
            self.sendMessage(json.dumps(message).encode('utf-8'))
            Logger.debug(f"{name}: send, {message}")
        else:
            Logger.debug(f"{name}: can't send")

    def onMessage(self, payload, isBinary):
        if not isBinary:
            data = json.loads(payload)
            Logger.debug(f"{name}: Got from server: {data}")
            if data.get("event"):
                Logger.error(data['event'])
                if data['event'] == 'on_message_create':
                    try:
                        message = createMessage(data['data'])
                    except Exception as E:
                        logging.error(E)
                    else:
                        self.factory.app.on_message(message)
                elif data['event'] == 'on_user_state_change':
                    """Эвент, когда НАС кто-то поменял, основное событие - с нами создали новый чат"""
                    if self.factory.app.check_new_chats(data):
                        self.onOpen()
                    

    def onClose(self, wasClean, code, reason):
        Logger.error(f"{name}: WebSocket connection closed {reason}")
        self.factory.app.reconnect()


class AppWebsocketClientFactory(WebSocketClientFactory):
    protocol = AppWebsocketClientProtocol

    def __init__(self, url, app):
        WebSocketClientFactory.__init__(self, url)
        self.app = app
