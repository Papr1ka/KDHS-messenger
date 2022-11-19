from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty, ObjectProperty

from kivymd.uix.list import OneLineIconListItem

class ProfilePopup(MDRelativeLayout):
    avatar_url = StringProperty("")
    display_name = StringProperty("")
    username = StringProperty("")
    status = StringProperty("")
    
    def __init__(self, **params):
        super().__init__()
        self.avatar_url = params.get("avatar_url", "")
        self.display_name = params.get("display_name", "")
        self.username = params.get("username", "")
        self.status = params.get("status", "")
