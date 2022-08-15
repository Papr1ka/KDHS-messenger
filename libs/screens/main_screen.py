from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.properties import ListProperty
from libs.components.text_input_round import TextInputRound
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.app import MDApp
from kivy.properties import StringProperty


class Contact(MDFloatLayout, HoverBehavior):
    
    text = StringProperty("")
    app = None
    
    def get_app(self):
        if not self.app:
            self.app = MDApp.get_running_app()
        return self.app
    
    def on_enter(self):
        app = MDApp.get_running_app()
        self.md_bg_color = self.get_app().colors['SecondColor']
    
    def on_leave(self):
        self.md_bg_color = self.get_app().colors['ThirdAccentColor']


class MainContactEventBehavior(MDScreen):
    
    data = ListProperty([{'text': 'алибаба'}])
    
    def on_enter(self):
        pass


class MainMobileView(MainContactEventBehavior):
    pass


class MainTabletView(MainContactEventBehavior):
    pass


class MainDesktopView(MainContactEventBehavior):
    pass


class MainScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MainMobileView()
        self.tablet_view = MainTabletView()
        self.desktop_view = MainDesktopView()
