from __future__ import unicode_literals
import asyncio
import json
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import DictProperty
from libs.server import Client
from kivy.app import async_runTouchApp

from settings import Templates, BASE_DIR, Logger
from libs.screen_manager.screen_manager import RootScreenManager
from libs.colors import colors
from libs.data import Data
from libs.snackcontroller import Controller
from libs.settings import Settings
from libs.notify import Notifier
import kivymd.utils.asynckivy as ak
from kivy.base import ExceptionHandler
from logging import config, getLogger
import sys


class KDHSMessengerApp(MDApp, Data, Settings):
    
    colors = DictProperty({})
    connection = None
    label = None
    
    def __init__(self, **kwargs):
        self.client = Client()
        self.controller = Controller()
        self.Logger = Logger
        self.notifier = Notifier()
        self.Logger.info("Initialized KDHS App")
        super().__init__(**kwargs)
    
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.colors.update(colors)
        self.__load_all_kv_files()
        self.__load_theme()
        self.screen_manager = RootScreenManager()
        root = self.screen_manager
        return root
    
    def __load_theme(self):
        
        self.colors = {i: get_color_from_hex(colors[i]) for i in colors}
        self.theme_cls.theme_style = 'Dark'
    
    def __load_all_kv_files(self):
        """
        - Method loads all .kv files of the project
        """
        for dir in Templates:
            for kvfile in dir.glob('*.kv'):
                self.Logger.info(kvfile.relative_to(BASE_DIR).__str__())
                Builder.load_file(kvfile.relative_to(BASE_DIR).__str__())


if __name__ == "__main__":
    # from twisted.python import log
    # log.startLogging(sys.stdout)
    KDHSMessengerApp().run()
