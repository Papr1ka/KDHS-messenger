from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from libs.screens.login_screen import LoginBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from libs.utils.checks import check_password_length
from libs.exceptions import AccessError
from libs.exceptions import UserExistsError, CommonPasswordError, ShortPasswordError


class MobileView(MDScreen):
    pass


class TabletView(MDScreen):
    pass


class DesktopView(MDScreen):
    pass


class RegisterBehavior(LoginBehavior):
    @property
    def password2(self):
        return self.children[-5].get_text()

    def register(self):
        if not self.password == self.password2:
            return self.show_error("Passwords must match")
        if not check_password_length(self.password):
            return self.show_error('Password must contain at least 8 characters')
        try:
            self.client.register(self.username, self.password)
        except CommonPasswordError:
            return self.show_error('This password is too common')
        except UserExistsError:
            return self.show_error('A user with that username already exists')
        except ShortPasswordError:
            return self.show_error('Password must contain at least 8 characters') 
        except AccessError:
            self.show_error('Invalid username or password')
        else:
            self.login()


class RegisterScreenBase(MDFloatLayout, RegisterBehavior):
    pass


class RegisterScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()
