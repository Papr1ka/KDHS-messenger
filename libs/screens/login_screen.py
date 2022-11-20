from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.floatlayout import MDFloatLayout
from libs.components.text_input_round import TextInputRoundIcon
from libs.utils.checks import check_password_length
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from libs.exceptions import AccessError
from libs.utils.behaviors import GetApp


class LoginMobileView(MDScreen):
    pass


class LoginTabletView(MDScreen):
    pass


class LoginDesktopView(MDScreen):
    pass


class LoginBehavior(GetApp):

    def show_error(self, message):
        self.ids.error.text = message
        self.ids.error.texture_update()
    
    @property
    def username(self):
        return self.children[-3].get_text()
    
    @property
    def password(self):
        return self.children[-4].get_text()

    def login(self):
        if not check_password_length(self.password):
            return self.show_error('Password must contain at least 8 characters')
        try:
            # self.client.autorize(self.username, self.password)
            flag = self.app.login('bob', 'qweqweqwe123')
        except AccessError:
            self.show_error('Invalid username or password')
        else:
            if flag:
                self.app.on_login()
                self.app.screen_manager.switch_screen('main_screen')


class LoginScreenBase(MDFloatLayout, LoginBehavior):
    pass
        


class LoginScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = LoginMobileView()
        self.tablet_view = LoginTabletView()
        self.desktop_view = LoginDesktopView()
