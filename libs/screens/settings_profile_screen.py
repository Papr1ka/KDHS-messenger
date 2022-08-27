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


class Meta():
    avatar_url = StringProperty("assets/icons/user.png")
    username = StringProperty("Loading...")
    date_created = StringProperty("Сейчас")


class ProfileCard(MDCard, Meta):
    pass


class SettingsProfileScreen(MDScreen, Meta, GetApp):

    def change_username(self, obj, text):
        try:
            self.app.change_username(text)
        except ValueError:
            show_error_snackbar("Такое имя пользователя уже занято")
        else:
            show_success_snackbar("Имя пользователя изменено")
    
    def select_path(self, path):
        self.exit_manager()
        if is_image(path):
            self.app.change_avatar(path)
            self.show_success_snackbar("Изображение успешно изменено")
        else:
            self.show_error_snackbar("Изображение/Файл не поддерживается")
    
    def change_avatar(self, button):
        self.file_manager.show(self.path)
    
    def exit_manager(self, *args):
        self.file_manager.close()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.path = str(BASE_DIR)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        Clock.schedule_once(self.bind_components, 1)
    
    def bind_components(self, tm):
        self.ids.username_item.textinput.bind(
            on_submit=self.change_username
        )
        self.ids.profile_card.ids.avatar.bind(
            on_press=self.change_avatar
        )
