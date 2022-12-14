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
            return self.show_error("Пароли должны совпадать")
        if not check_password_length(self.password):
            return self.show_error('Пароль должен состоять не менее чем из 8 символов')
        try:
            flag = self.app.register(self.username, self.password)
        except CommonPasswordError:
            return self.show_error('Слишком слабый пароль')
        except UserExistsError:
            return self.show_error('Пользователь с таким именем уже существует')
        except ShortPasswordError:
            return self.show_error('Пароль должен состоять не менее чем из 8 символов') 
        except AccessError:
            self.show_error('Неправильный логин, или пароль')
        else:
            if flag:
                self.app.screen_manager.switch_screen('main_screen')


class RegisterScreenBase(MDFloatLayout, RegisterBehavior):
    pass


class RegisterScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()
