from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.floatlayout import MDFloatLayout
from libs.components.text_input_round import TextInputRoundIcon
from libs.utils.checks import check_password_length
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from libs.exceptions import AccessError


class LoginMobileView(MDScreen):
    pass


class LoginTabletView(MDScreen):
    pass


class LoginDesktopView(MDScreen):
    pass


class LoginBehavior():

    _client = None
    _app = None

    def show_error(self, message):
        self.ids.error.text = message
        self.ids.error.texture_update()
    
    @property
    def app(self):
        if not self._app:
            self._app = MDApp.get_running_app()
        return self._app
    
    @property
    def client(self):
        if not self._client:
            self._client = self.app.client
        return self._client
    
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
            #self.client.autorize(self.username, self.password)
            self.client.autorize('bob', 'qweqweqwe123')
        except AccessError:
            self.show_error('Invalid username or password')
        else:
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
