from __future__ import unicode_literals
import asyncio
import json
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import DictProperty
from libs.server import Client
from libs.user import User
from kivy.app import async_runTouchApp

from settings import Templates, BASE_DIR
from libs.screen_manager.screen_manager import RootScreenManager
from libs.colors import colors
from libs.data import Data
from libs.settings import Settings
import kivymd.utils.asynckivy as ak




from kivy.support import install_twisted_reactor
install_twisted_reactor()

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


from twisted.internet import reactor







class KDHSMessengerApp(MDApp, Data, Settings):
    
    colors = DictProperty({})
    connection = None
    textbox = None
    label = None
    
    def __init__(self, **kwargs):
        self.client = Client()
        super().__init__(**kwargs)
    
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.colors.update(colors)
        self.__load_all_kv_files()
        self.__load_theme()
        self.screen_manager = RootScreenManager()
        root = self.screen_manager
        self.connect_to_server()

        return self.screen_manager

    def connect_to_server(self):
        # self._factory = MyKivyClientFactory("ws://127.0.0.1:8000/ws/messages/?token=0d2fbbd2e568294cd3b95471388275e300e51a93", self)
        # reactor.connectTCP('127.0.0.1', 8000, self._factory)
        # # self.send_message(json.dumps({
        # #     'pk': "3",
        # #     'action': "start_listen",
        # #     'request_id': 123,
        # # }))
        # print("connected")
        print("pass")
    
    # def send_message(self, *args):
    #     """
    #     Send the text entered that was entered in the texbox widget.
    #     """
    #     msg = "abc"
    #     proto = self._factory._proto
    #     if msg and proto:
    #         proto.sendMessage(msg)
    #         self.print_message('Sent to server: {}'.format(self.textbox.text))
    #     else:
    #         print("cant send")

    def print_message(self, msg):
        print(msg)
    
    def __load_theme(self):
        
        self.colors = {i: get_color_from_hex(colors[i]) for i in colors}
        self.theme_cls.theme_style = 'Dark'
    
    def __load_all_kv_files(self):
        """
        - Method loads all .kv files of the project
        """
        for dir in Templates:
            for kvfile in dir.glob('*.kv'):
                print(kvfile.relative_to(BASE_DIR).__str__())
                Builder.load_file(kvfile.relative_to(BASE_DIR).__str__())


if __name__ == "__main__":
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)
    KDHSMessengerApp().run()
