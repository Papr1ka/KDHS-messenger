from libs.chat import Chat
from libs.exceptions import ServerError
from libs.message import Message
from libs.models import *
from libs.user import User
from libs.server import Client
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from libs.utils.window import get_window_type
from kivy.uix.label import Label
from libs.utils.protocols import MyKivyClientFactory
from twisted.internet import reactor
from kivymd.app import MDApp


class Data():
    
    client: Client
    app: MDApp
    self_user: User = None
    #данные для контактов, зеркало для display_viewset
    contacts: list[ChatModel] = ListProperty([])
    #те данные, которые должны отображаться в данный момент
    display_viewset: list[dict[Union[ChatViewModel, ContactViewModel]]] = ListProperty([])
    #сохранённые данные контактов
    contacts_viewset: list[dict[Union[ChatViewModel, ContactViewModel]]] = ListProperty([])
    contacts_loaded: bool = False
    messages = ListProperty([])
    chats = {}
    selected_chat_id = StringProperty("")
    current_destination_username = StringProperty("")
    current_destination_avatar_url = StringProperty("assets/icons/user.png")
    current_username = StringProperty("TheLastPapr1ka")
    current_avatar_url = StringProperty("assets/icons/user.png")
    current_date_created = StringProperty("Now")
    connection: MyKivyClientFactory

    def on_login(self):
        print("on_login")
        self.self_user = self.get_self_user()
        self.current_username = self.self_user.username
        self.current_avatar_url = self.self_user.avatar_url
        self.current_date_created = self.self_user.date_created.strftime("%d:%m:%Y")
        self.load_contacts()
        self.show_contacts()
        print(self.contacts)
        print(self.contacts_viewset)
        print(self.display_viewset)
        self.app = MDApp.get_running_app()
        # self.connection = MyKivyClientFactory("ws://127.0.0.1:8000/ws/messages/?token=0d2fbbd2e568294cd3b95471388275e300e51a93", self.app)
        # reactor.connectTCP('127.0.0.1', 8000, self.app._factory)
        # print("connected")


    def on_sign_out(self):
        print("on_sign_out")
        self.self_user = None
        self.contacts = []
        self.contacts_loaded = False
        self.contacts_viewset = []
        self.selected_chat_id = ""
        self.current_destination_username = ""
        self.current_destination_avatar_url = "assets/icons/user.png"
        self.current_username = ""
        self.current_avatar_url = "assets/icons/user.png"
        self.messages = []
        self.chats = {}
    
    def search_contacts(self, username: str):
        try:
            users: list[UserModel] = self.client.searchUsers(username)
        except ServerError:
            viewset = []
        else:
            viewset = [asdict(createContact(user)) for user in users]
        self.display_viewset.clear()
        self.display_viewset = viewset
        print("обновил")
    
    def show_contacts(self):
        self.display_viewset.clear()
        self.display_viewset = self.contacts_viewset
        print(self.display_viewset)
    
    def create_chat(self, user_id: int):
        print(user_id)
        print("create chat")
        try:
            chat = self.client.createchat(str(user_id))
        except Exception as E:
            print("Не судьба", E)
        else:
            try:
                user = self.client.getuser(str(user_id))
            except Exception as E:
                print("Не удалось найти пользователя", E)
            else:
                chat = ChatModel(chat.id, chat.messages, chat.created_at, chat.users, user.username, user.id, "", user.avatar_image)
                self.contacts.insert(0, chat)
                self.contacts_viewset.insert(0, asdict(createChatView(chat)))
                self.show_contacts()
                self.on_chat_switch(str(chat.id))

    def get_self_user(self):
        if self.self_user is None:
            data = self.client.getMe()
            self.self_user = User().from_data(data)
            return self.self_user
        return self.self_user
    
    def load_contacts(self):
        if not self.contacts_loaded:
            data = self.client.getcontacts()['chats']['chats']
            self.contacts.clear()
            for chat in data:
                chat_model = createChat(chat)
                self.contacts.append(chat_model)
                self.contacts_viewset.append(asdict(createChatView(chat_model)))
            self.contacts_loaded = True
    
    def get_messages(self, chat_id: str):
        story_exists = self.chats.get(chat_id, None)
        if not story_exists:
            messages = self.client.getmessagelist(chat_id, '1')['messages']
            for i in messages:
                self.add_message({'text': i['text']}, from_me=False if str(self.get_self_user().id) != i['author_id'] else True)
        else:
            self.messages = self.chats[chat_id]
    
    def find_contact_by_chat_id(self, chat_id):
        for i in self.contacts:
            if str(i.id) == chat_id:
                return i

    def find_contact_view_by_chat_id(self, chat_id):
        for i in self.contacts_viewset:
            if i['id'] == chat_id:
                return i
    
    def on_chat_switch(self, chat_id: str):
        print("on_chat_switch")
        self.selected_chat_id = chat_id
        self.current_destination_username = self.find_contact_by_chat_id(self.selected_chat_id).destination_username
        self.messages = []
        self.get_messages(chat_id)
    
    def add_message(self, data: dict, from_me=True):
        if from_me:
            data.update({'pos_hint': {'right': 1}, 'halign': 'right', 'send_by_user': True})
        else:
            data.update({'pos_hint': {'x': 0}, 'halign': 'left', 'send_by_user': False})
        l = Label(text=data['text'], markup=False)
        l.texture_update()
        data.update({'max_text_width': l.texture_size[0] * 1.08})
        self.messages.append(data)
        self.story_message(data)
    
    def story_message(self, data: dict):
        if self.selected_chat_id != '':
            story_exists = self.chats.get(self.selected_chat_id, None)
            if not story_exists:
                self.chats[self.selected_chat_id] = []
            self.chats[self.selected_chat_id].append(data)
    
    def send_message(self, message: str):
        if self.selected_chat_id != '':
            data = self.client.sendmessage(self.selected_chat_id, message)
            msg = Message().from_data(data)
            self.add_message({'text': message}, from_me=True)
            self.change_chat_last_message(msg, self.selected_chat_id)
    
    def change_chat_last_message(self, message: Message, chat_id):
        contact = self.find_contact_by_chat_id(chat_id)
        if contact:
            contact.last_message = message
            self.contacts_viewset.remove(self.find_contact_view_by_chat_id(chat_id))
            self.contacts_viewset.insert(0, asdict(createChatView(contact)))

    def change_username(self, username):
        self.client.change_username(username)
        self.current_username = username

    def change_avatar(self, path_to_image):
        self.client.change_avatar(path_to_image)
        self.self_user = None
        self.self_user = self.get_self_user()
        self.current_avatar_url = self.self_user.avatar_url
