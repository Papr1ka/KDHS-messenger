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

from libs.components.profile_popup import ProfilePopup
from libs.components.text_input_round import TextInputRound, TextInputString
from libs.components.chat_bubble import ChatBubble
from libs.components.listitem import ChatListItem
from libs.exceptions import ServerError
from libs.utils.behaviors import GetApp
from libs.components.chat_create_popup import ChatCreatePopup


class ChatItem(ChatListItem):
    def on_touch_down(self, touch):
        if self.app and self.collide_point(touch.x, touch.y):
            self.open_messages()
    
    def open_messages(self):
        screen = self.app.screen_manager.adaptive_switch_screen('messages_screen', self.app.root)
        self.app.on_chat_switch(self.chat_id)


class ContentNavigationDrawer(MDBoxLayout):
    pass


class MainContactEventBehavior(GetApp):
    
    contacts = ListProperty([])

class SidebarNavigation(MDNavigationDrawer, MainContactEventBehavior):
    back_color = ColorProperty((0, 0, 0, 1))
    header_head = StringProperty("")
    icon_source = StringProperty("")
    dialog_username = None
    dialog_chat = None
    
    def sign_out(self):
        self.app.screen_manager.switch_screen("login_screen")
        self.app.on_sign_out()
    
    
    def show_username_change_dialog(self, *args):
        
        popup = ProfilePopup(
            avatar_url=self.app.current_avatar_url,
            display_name="Кирилл",
            username=self.app.current_username,
            status="Бог"
        )
        
        if not self.dialog_username:
            self.dialog_username = MDDialog(
                md_bg_color=self.app.colors["SearchColor"],
                title="Информация",
                type="custom",
                content_cls=popup,
                width_offset=0,
            )
        self.dialog_username.open()


    def show_chat_create_dialog(self):
        if not self.dialog_chat:
            self.dialog_chat = MDDialog(
                title="Address:",
                type="custom",
                content_cls=ChatCreatePopup(),
                buttons=[
                    MDFlatButton(
                        text="Отменить",
                        theme_text_color="Custom",
                        text_color=self.app.colors["MainColor"],
                        radius=[dp(18)]
                    ),
                    MDFlatButton(
                        text="Найти",
                        theme_text_color="Custom",
                        text_color=self.app.colors["MainColor"],
                        radius=[dp(18)],
                        on_release=self.find_user
                    ),
                ],
            )
        self.dialog_chat.open()
    
    def find_user(self, *args):
        print(args)
        if self.dialog_chat:
            username = self.dialog_chat.content_cls.ids.username.text
            try:
                user = self.app.client.searchUser(username)
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
    pass


class MainScreen(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MainMobileView()
        self.tablet_view = MainTabletView()
        self.desktop_view = MainDesktopView()
