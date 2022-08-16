from libs.user import User
from libs.server import Client
from kivymd.app import MDApp
from kivy.properties import ObjectProperty

class Data():
    
    client: Client
    app: MDApp
    self_user: User = None
    
    def __init__(self) -> None:
        print("on___init__")

    def on_login(self):
        print("on_login")
        self.self_user = self.get_self_user()
        print("on_login_end")
    
    def get_self_user(self):
        if not self.self_user:
            data = self.client.getMe()
            self.self_user = User().from_data(data)
            return self.self_user
        return self.self_user
