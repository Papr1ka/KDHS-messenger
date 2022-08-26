from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior

from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineAvatarIconListItem, IRightBody
from kivymd.app import MDApp
from kivy.clock import Clock


class ChatListItem(TwoLineAvatarIconListItem, HoverBehavior):
    image = StringProperty()
    bg_color = ColorProperty([0, 0, 0, 0])
    text = StringProperty()
    secondary_text = StringProperty()
    time = StringProperty()
    
    app = None
    
    def get_app(self):
        if not self.app:
            self.app = MDApp.get_running_app()
        return self.app

    def on_enter(self):
        self.bg_color = self.get_app().colors['SecondColor']
    
    def on_leave(self):
        self.bg_color = self.get_app().colors['ThirdAccentColor']


class RightTime(IRightBody, MDLabel):
    pass
