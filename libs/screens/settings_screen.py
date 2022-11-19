from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.clock import Clock

from libs.utils.behaviors import GetApp
from libs.components.snackbar import show_error_snackbar, show_success_snackbar
from kivymd.uix.filemanager import MDFileManager
from libs.utils.checks import is_image
from libs.exceptions import InvalidDisplayNameError, InvalidStatusError

class MyToggleButton(MDFlatButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SettingsScreenBase(MDRelativeLayout):
    pass


class SettingsBehavior(GetApp):
    dialog = None
    
    path = '/'
    
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
    
    def change_status(self, instance):
        if instance.text != "":
            try:
                self.app.change_user_data({'status': instance.text})
            except InvalidStatusError:
                show_error_snackbar("Статус введён некорректно")
            else:
                show_success_snackbar("Статус успешно измененён")
    
    def change_display_name(self, instance):
        if instance.text != "":
            try:
                self.app.change_user_data({'display_name': instance.text})
            except InvalidDisplayNameError:
                show_error_snackbar("Имя введено некорректно")
            else:
                show_success_snackbar("Имя успешно изменено")

    def change_font_size(self, instance):
        font_size = instance.text
        try:
            font_size = int(font_size)
        except (TypeError, ValueError):
            show_error_snackbar("Шрифт должен быть от 12 до 40")
        else:
            if 12 <= font_size <= 40:
                self.app.change_font_size(font_size)
                show_success_snackbar("Шрифт успешно изменён")
            else:
                show_error_snackbar("Шрифт должен быть от 12 до 40")
    
    def bind_components(self, tm):
        self.ids.base.ids.avatar.bind(
            on_press=self.change_avatar
        )
        self.ids.base.ids.status.bind(
            on_text_validate=self.change_status
        )
        self.ids.base.ids.display_name.bind(
            on_text_validate=self.change_display_name
        )
        self.ids.base.ids.font_size.bind(
            on_text_validate=self.change_font_size
        )


class SettingsMobileView(MDScreen, SettingsBehavior):
    pass


class SettingsTabletView(MDScreen, SettingsBehavior):
    pass


class SettingsDesktopView(MDScreen, SettingsBehavior):
    pass


class SettingsToolbar(MDTopAppBar, GetApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.left_action_items = [["arrow-left", lambda x: self.app.screen_manager.switch_screen('main_screen')]]


class SettingsScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = SettingsMobileView()
        self.tablet_view = SettingsTabletView()
        self.desktop_view = SettingsDesktopView()
