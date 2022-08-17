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
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.widget import MDAdaptiveWidget

from libs.components.text_input_round import TextInputRound, TextInputString
from libs.components.chat_bubble import ChatBubble
from libs.components.listitem import ChatListItem
from kivy.clock import Clock


class ChatItem(ChatListItem):
    def on_touch_down(self, touch):
        if self.app and self.collide_point(touch.x, touch.y):
            self.open_messages()
    
    def open_messages(self):
        screen = self.app.screen_manager.adaptive_switch_screen('messages_screen', self.app.root)
        self.app.on_chat_switch(self.chat_id)


class ContentNavigationDrawer(MDBoxLayout):
    pass


class MainContactEventBehavior():
    
    #data = ListProperty([{'text': "Алибаба", 'icon_source': "assets/icons/user.png"}])
    contacts = ListProperty([])
    _app = None
    
    @property
    def app(self):
        if not self._app:
            self._app = MDApp.get_running_app()
        return self._app
    
    def on_login(self):
        self.ids.nav_drawer.header_head = self.app.get_self_user().username
        user_data = {
            "text": "Thomas Brewer",
            "secondary_text": "Hey kivy is really awesome!",
            "time": "9:02",
            "image": "assets/icons/user.png",
            "unread_messages": True,
            "on_release": lambda x: print(),
        }
        #{'text': i.destination_username, 'icon_source': "assets/icons/user.png"}
        self.contacts = [{'text': i.destination_username,
                          'image': "assets/icons/user.png",
                          'unread_messages': True,
                          'secondary_text': '' if not i.last_message else i.last_message.text,
                          'time': '18:00',
                          'chat_id': str(i.id)} for i in self.app.get_contacts()]
    
    def on_sign_out(self):
        self.contacts = []


class SidebarNavigation(MDNavigationDrawer, MainContactEventBehavior):
    back_color = ColorProperty((0, 0, 0, 1))
    header_head = StringProperty("")
    header_body = StringProperty("")
    icon_source = StringProperty("")
    
    def sign_out(self):
        self.app.screen_manager.switch_screen("login_screen")
        self.app.on_sign_out()

class MainMobileView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainTabletView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainDesktopView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MessagesBehavior():
    messages: list = []
    _app = None
    
    @property
    def app(self):
        if not self._app:
            self._app = MDApp.get_running_app()
        return self._app
    
    def send_from_button(self, button):
        self.send_message(button.parent.textinput)
    
    def send_message(self, instance_textfield):
        text = instance_textfield.text
        if text != '':
            self.app.send_message(text)
            instance_textfield.text = ''
    
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.bind_components, 1)
    
    def bind_components(self, x):
        self.messages = self.app.messages
        self.ids.text_input.textinput.bind(
            on_text_validate=self.send_message
        )
        self.ids.text_input.button.bind(
            on_press=self.send_from_button
        )
        self.ids.messages_rv.data = self.messages


class MessagesLayout(RelativeLayout, MDAdaptiveWidget, MessagesBehavior):
    pass

class MessagesScreen(MDScreen, MessagesBehavior):
    
    def on_enter(self):
        print(self.ids)


class MainScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MainMobileView()
        self.tablet_view = MainTabletView()
        self.desktop_view = MainDesktopView()
    
    def on_login(self):
        self.mobile_view.on_login()
        self.tablet_view.on_login()
        self.desktop_view.on_login()
    
    def on_sign_out(self):
        self.mobile_view.on_sign_out()
        self.tablet_view.on_sign_out()
        self.desktop_view.on_sign_out()
