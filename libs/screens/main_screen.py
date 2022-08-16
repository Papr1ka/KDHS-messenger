from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.properties import ListProperty, ColorProperty, StringProperty, OptionProperty, DictProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.label import MDLabel

from libs.components.text_input_round import TextInputRound, TextInputString
from libs.components.chat_bubble import ChatBubble


class ContentNavigationDrawer(MDBoxLayout):
    pass


class SidebarNavigation(MDNavigationDrawer):
    back_color = ColorProperty((0, 0, 0, 1))
    header_head = StringProperty("")
    header_body = StringProperty("")
    icon_source = StringProperty("")
    _app = None
    
    @property
    def app(self):
        if not self._app:
            self._app = MDApp.get_running_app()
        return self._app
    
    def get_header(self):
        return self.app.user.username
    


class Contact(MDFloatLayout, HoverBehavior):
    
    text = StringProperty("")
    icon_source = StringProperty("")
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
    
    def on_touch_down(self, touch):
        if self.app and self.collide_point(touch.x, touch.y):
            self.open_messages()
    
    def open_messages(self):
        self.app.screen_manager.switch_screen('messages_screen')


class MainContactEventBehavior(MDScreen):
    
    data = ListProperty([{'text': "Алибаба", 'icon_source': "assets/icons/user.png"}])
    
    def on_enter(self):
        print("on_enter")


class MainMobileView(MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainTabletView(MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainDesktopView(MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MessagesScreen(MDScreen):
    pass


class MainScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MainMobileView()
        self.tablet_view = MainTabletView()
        self.desktop_view = MainDesktopView()
    
    def on_enter(self):
        print("on_enter")
