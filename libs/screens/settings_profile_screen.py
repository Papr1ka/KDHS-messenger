from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivymd.uix.filemanager import MDFileManager

from libs.utils.behaviors import GetApp
from libs.utils.checks import is_image
from libs.components.snackbar import show_error_snackbar, show_success_snackbar


class Meta():
    avatar_url = StringProperty("assets/icons/user.png")
    username = StringProperty("Loading...")
    date_created = StringProperty("Сейчас")


class ProfileCard(MDCard, Meta):
    pass


class SettingsProfileScreen(MDScreen, Meta, GetApp):
    
    path = '/'

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
            show_success_snackbar("Изображение успешно изменено")
        else:
            show_error_snackbar("Изображение/Файл не поддерживается")
    
    def change_avatar(self, button):
        self.file_manager.show(self.path)
    
    def exit_manager(self, *args):
        self.path = self.file_manager.current_path
        self.file_manager.close()

    def __init__(self, **kw):
        super().__init__(**kw)
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
