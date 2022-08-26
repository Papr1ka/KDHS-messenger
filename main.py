from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import DictProperty
from libs.server import Client
from libs.user import User

from settings import Templates, BASE_DIR
from libs.screen_manager.screen_manager import RootScreenManager
from libs.colors import colors
from libs.data import Data


class KDHSMessengerApp(MDApp, Data):
    
    colors = DictProperty({})
    
    def __init__(self, **kwargs):
        self.client = Client()
        super().__init__(**kwargs)
    
    def build(self):
        self.theme_cls.colors.update(colors)
        self.__load_all_kv_files()
        self.__load_theme()
        self.screen_manager = RootScreenManager()

        return self.screen_manager
    
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
    KDHSMessengerApp().run()
