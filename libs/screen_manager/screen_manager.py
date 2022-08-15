import imp
from kivy.uix.screenmanager import ScreenManager
from libs.screens.login_screen import LoginScreen
from libs.screens.register_screen import RegisterScreen
from libs.screens.main_screen import MainScreen
from kivymd.uix.screen import Screen

class RootScreenManager(ScreenManager):
    def switch_screen(self, screen_name) -> Screen:
        """Changes the current screen to the screen with the name screen_name

        Args:
            screen_name (__str__): screen name to redirect to

        Raises:
            ValueError: Raised when the screen with the name screen_name is not found
        """
        if not self.has_screen(screen_name):
            raise ValueError(f"Screen {screen_name} not found")
        self.current = screen_name
