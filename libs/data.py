from libs.chat import Chat
from libs.user import User
from libs.server import Client
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from libs.utils.window import get_window_type

class Data():
    
    client: Client
    app: MDApp
    self_user: User = None
    contacts: list = []
    contacts_loaded: bool = False
    messages = ListProperty([])
    chats = {}
    selected_chat_id = StringProperty("")
    current_destination_username = StringProperty("")

    def on_login(self):
        print("on_login")
        self.self_user = self.get_self_user()
        self.root.ids.main_screen.on_login()
        self.contacts = self.get_contacts()
    
    def on_sign_out(self):
        print("on_sign_out")
        self.self_user = None
        self.contacts = []
        self.contacts_loaded = False
        self.selected_chat_id = ""
        self.current_destination_username = ""
        self.messages = []
        self.chats = {}
        self.root.ids.main_screen.on_sign_out()
    
    def get_self_user(self):
        if self.self_user is None:
            data = self.client.getMe()
            self.self_user = User().from_data(data)
            return self.self_user
        return self.self_user
    
    def get_contacts(self):
        if not self.contacts_loaded:
            data = self.client.getcontacts()['chats']['chats']
            for chat in data:
                self.contacts.append(Chat().from_data(chat))
            self.contacts_loaded = True
            print(len(self.contacts))
            return self.contacts
        return self.contacts
    
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
            self.client.sendmessage(self.selected_chat_id, message)
            self.add_message({'text': message}, from_me=True)
