from kivymd.app import MDApp
from kivy.lang.builder import Builder

from settings import Templates, BASE_DIR
from libs.screen_manager.screen_manager import RootScreenManager


class KDHSMessengerApp(MDApp):
    def build(self):
        self.__load_all_kv_files()
        self.__load_theme()
        return RootScreenManager()
    
    def __load_theme(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "BlueGray"
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
