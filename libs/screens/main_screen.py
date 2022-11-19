from kivymd.uix.screen import MDScreen
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.properties import ListProperty, ColorProperty, StringProperty, OptionProperty, DictProperty
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.widget import MDAdaptiveWidget
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp
from kivymd.uix.toolbar import MDTopAppBar

from libs.components.profile_popup import ProfilePopup
from libs.components.text_input_round import TextInputRound, TextInputString
from libs.components.chat_bubble import ChatBubble
from libs.components.listitem import ChatListItem
from libs.exceptions import ServerError
from libs.utils.behaviors import GetApp
from libs.models import *


class Bar(MDTopAppBar, GetApp):
    def on_touch_down(self, touch):
        print(self.app.current_destination_username)
        if self.collide_point(touch.x, touch.y):
            print(self.app.current_destination_username)


class ChatItem(ChatListItem):
    
    def on_touch_down(self, touch):
        if self.app and self.collide_point(touch.x, touch.y):
            self.open_messages()
            print(self.text)
            print(self.chat_id)
    
    def open_messages(self):
        print(self.__dict__)
        print(self.viewclass)
        screen = self.app.screen_manager.adaptive_switch_screen('messages_screen', self.app.root)
        try:
            self.app.on_chat_switch(self.chat_id)
        except AttributeError as E:
            print(E)
            self.app.create_chat(self.id)
            
            print("вызвал функцию, отработала")


class ContentNavigationDrawer(MDBoxLayout):
    pass


class MainContactEventBehavior(GetApp):
    
    # contacts = ListProperty([])
    
    def __init__(self) -> None:
        super().__init__()
        Clock.schedule_once(self.bind_components, 1)
    
    def bind_components(self, tm):
        if self.ids.get("search"):
            self.ids.search.textinput.bind(
                on_text_validate=self.search
            )
    
    def search(self, textinput):
        query = textinput.text
        if query != '':
            self.app.search_contacts(query)
        else:
            self.app.show_contacts()

class SidebarNavigation(MDNavigationDrawer, MainContactEventBehavior):
    back_color = ColorProperty((0, 0, 0, 1))
    header_head = StringProperty("")
    icon_source = StringProperty("")
    
    def sign_out(self):
        self.app.screen_manager.switch_screen("login_screen")
        self.app.on_sign_out()
    
    
    def show_profile_dialog(self, *args):
        
        popup = ProfilePopup(
            avatar_url=self.app.current_avatar_url,
            display_name=self.app.current_display_name,
            username=self.app.current_username,
            status=self.app.current_status
        )
        
        dialog = MDDialog(
            md_bg_color=self.app.colors["SearchColor"],
            title="Информация",
            type="custom",
            content_cls=popup,
            width_offset=0,
        )
        dialog.open()
    
    def find_user(self, *args):
        print(args)
        if self.dialog_chat:
            username = self.dialog_chat.content_cls.ids.username.text
            try:
                user = self.app.client.searchUsers(username)
            except ServerError:
                pass
            else:
                print("нашёл")
                print(user)
        else:
            print("что?")

class MainMobileView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainTabletView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MainDesktopView(MDScreen, MainContactEventBehavior):
    def on_enter(self):
        super().on_enter()


class MessagesBehavior(GetApp):
    messages: list = []
    dialog = None
    
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
    
    
    def show_user_profile(self):
        chat = self.app.find_contact_by_chat_id(self.app.selected_chat_id)
        user: Union[UserModel, None] = self.app.get_user(chat.users[-1])
        if user:
            print(user)
        
            popup = ProfilePopup(
                avatar_url=user.avatar_image,
                display_name=user.display_name,
                username=user.username,
                status=user.status if user.status != "" else "Всем привет, я использую WhatsApp!",
            )
            
            dialog = MDDialog(
                    md_bg_color=self.app.colors["SearchColor"],
                    title="Информация",
                    type="custom",
                    content_cls=popup,
                    width_offset=0,
                )
            dialog.open()
        


class MessagesLayout(RelativeLayout, MDAdaptiveWidget, MessagesBehavior):
    pass

class MessagesScreen(MDScreen, MessagesBehavior):
    pass


class MainScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MainMobileView()
        self.tablet_view = MainTabletView()
        self.desktop_view = MainDesktopView()
