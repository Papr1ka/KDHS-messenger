from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout, MDAdaptiveWidget
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from libs.utils.behaviors import GetApp
from libs.components.textfield_popup import TextFieldPopup


class SettingsScreenBase(MDRelativeLayout):
    pass


class SettingsBehavior(GetApp):
    username = "Loading..."
    font_size = "18"
    dialog = None
    
    def on_login(self):
        self.ids.base.ids.avatar_image.source = self.app.get_self_user().avatar_url
        self.username = self.app.get_self_user().username
        self.ids.base.ids.username_header.text = self.username
        # self.ids.base.ids.username.secondary_text = self.username
        # self.ids.base.ids.font_size.secondary_text = "18"
        pass
    
    def show_username_change_dialog(self, ):

        def close_dilog(obj):
            self.dialog.dismiss()
        
        def use_input(obj):
            text = self.dialog.content_cls.get_text()
            print(text)

        if not self.dialog:
            self.dialog = MDDialog(
                title="Username",
                type="custom",
                content_cls=TextFieldPopup(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.app.colors['SecondAccentColor'],
                        on_press = close_dilog
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.app.colors['SecondAccentColor'],
                        on_press = use_input
                    ),
                ],
            )
        self.dialog.open()

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

    def on_login(self):
        self.mobile_view.on_login()
        self.tablet_view.on_login()
        self.desktop_view.on_login()
