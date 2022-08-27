from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.filemanager import MDFileManager

from libs.components.settings_item import SettingsItem
from libs.utils.behaviors import GetApp
from libs.utils.checks import is_image
from libs.components.snackbar import show_error_snackbar, show_success_snackbar
from settings import BASE_DIR


class ProfileCard(MDCard):
    pass


class SettingsChatScreen(MDScreen, GetApp):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.bind_components, 1)
    
    def change_font_size(self, text_input, font_size: str):
        try:
            font_size = int(font_size)
        except TypeError:
            show_error_snackbar("Шрифт должен быть числом от 12 до 40")
        else:
            if 12 <= font_size <= 40:
                self.app.change_font_size(font_size)
                show_success_snackbar("Шрифт успешно изменён")
            else:
                show_error_snackbar("Шрифт должен быть от 12 до 40")
    
    def bind_components(self, tm):
        self.ids.font_item.textinput.bind(
            on_submit=self.change_font_size
        )
