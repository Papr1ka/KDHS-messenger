from libs.chat import Chat
from libs.exceptions import AccessError, InvalidDisplayNameError, InvalidStatusError, ServerError
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
    self_user: UserModel = None

    contacts: list[ChatModel] = ListProperty([])
    """
    contacts - список чатов, в каждом из которых находятся данные типа ChatModel
    нужен для того, чтобы брать оттуда информацию из отрендеренных чатов
    """
    
    display_viewset: list[dict[Union[ChatViewModel, ContactViewModel]]] = ListProperty([])
    """
    display_viewset - список отображаемых элементов в данный момент,
    при изменении списка - меняется набор отображаемых элементов в live режиме,
    для работы каждый элемент обращается к contacts
    """
    
    #сохранённые данные контактов
    contacts_viewset: list[dict[Union[ChatViewModel, ContactViewModel]]] = ListProperty([])
    """
    contacts_viewset - список готовых наборов данных для отображения контактов в формате словаря
    """
    messages = ListProperty([])
    """
    messages - список отображаемых сообщений
    """
    contacts_loaded: bool = False
    chats = {}
    selected_chat_id = StringProperty("")
    current_destination_username = StringProperty("")
    current_destination_avatar_url = StringProperty("assets/icons/user.png")
    
    #о нас
    current_username = StringProperty("")
    current_display_name = StringProperty("")
    current_status = StringProperty("")
    current_avatar_url = StringProperty("assets/icons/user.png")
    current_date_created = StringProperty("Now")
    
    connection: MyKivyClientFactory

    def on_login(self):
        print("on_login")
        self.self_user = self.get_self_user()
        self.current_username = self.self_user.username
        self.current_avatar_url = self.self_user.avatar_image
        print(self.self_user.date_joined)
        self.current_date_created = self.self_user.date_joined.strftime("%d:%m:%Y")
        self.current_display_name = self.self_user.display_name
        self.current_status = self.self_user.status
        self.load_contacts()
        self.show_contacts()
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
        except (ServerError, AccessError):
            self.display_viewset.clear()
        else:
            viewset = []
            for user in users:
                exists = False
                for contact in self.contacts:
                    if contact.users[-1] == user.id:
                        viewset.append(asdict(createChatView(contact)))
                        exists = True
                        break
                if not exists:
                    viewset.append(asdict(createContact(user)))
            
            self.display_viewset.clear()
            self.display_viewset = viewset
        print("обновил")
        print(self.display_viewset)
    
    def show_contacts(self):
        """
        Показывает контакты
        Заменяет данные из display_viewset на данные из contacts_viewset
        """
        self.display_viewset.clear()
        self.display_viewset = self.contacts_viewset
    
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
                view = asdict(createChatView(chat))
                self.contacts_viewset.insert(0, view)
                old_contact = self.find_display_view_by_chat_id(user_id)
                self.display_viewset.remove(old_contact)
                self.display_viewset.insert(0, view)
                self.on_chat_switch(str(chat.id))

    def get_self_user(self):
        if self.self_user is None:
            self.self_user = self.client.getMe()
            return self.self_user
        return self.self_user
    
    def load_contacts(self):
        """
        Получает список контактов с сервера, загружает модели ChatModel в список contacts, ChatModelView в список contacts_viewset
        """
        try:
            data = self.client.getcontacts()['chats']['chats']
        except ServerError:
            print("ошибка сервера")
        except AccessError:
            print("ошибка доступа")
        except Exception as E:
            print("ошибка", E)
        else:
            self.contacts.clear()
            for chat in data:
                chat_model = createChat(chat)
                self.contacts.append(chat_model)
                self.contacts_viewset.append(asdict(createChatView(chat_model)))
    
    def get_messages(self, chat_id: str):
        """
        Получает список сообщений для чата с id - chat_id, если история сообщений существует, загружает с неё, если нет - с сервера
        """
        story_exists = self.chats.get(chat_id, None)
        if not story_exists:
            messages = self.client.getmessagelist(chat_id, '1')
            for message in messages:
                self.add_message(message.text, from_me=False if str(self.get_self_user().id) != message.author_id else True)
        else:
            self.messages = self.chats[chat_id]
    
    def find_contact_by_chat_id(self, chat_id) -> ChatModel:
        for chat_model in self.contacts:
            if chat_model.id.__str__() == chat_id:
                return chat_model

    def find_contact_view_by_chat_id(self, chat_id):
        for i in self.contacts_viewset:
            if i['id'] == chat_id:
                return i
    
    def find_display_view_by_chat_id(self, chat_id):
        for i in self.display_viewset:
            if i['id'] == chat_id:
                return i
    
    def on_chat_switch(self, chat_id: str):
        """
        Меняет название для выбранного чата, id выбранного чата, загружает список сообщений для выбранного чата
        """
        print("on_chat_switch")
        self.selected_chat_id = chat_id
        self.current_destination_username = self.find_contact_by_chat_id(chat_id).destination_username
        self.messages = []
        self.get_messages(chat_id)
    
    def add_message(self, content: str, from_me=True):
        """
        Добавляет сообщение в список отображаемых сообщений, сохраняет в словарь сохранённых сообщений
        """
        data = {
            'text': content
        }
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
        """
        Добавляет данные для отображения сообщения в конкретный чат
        """
        if self.selected_chat_id != '':
            story_exists = self.chats.get(self.selected_chat_id, None)
            if not story_exists:
                self.chats[self.selected_chat_id] = []
            self.chats[self.selected_chat_id].append(data)
    
    def send_message(self, message: str):
        """
        Если выбран чат, отправляет сообщение на сервер,
        добавляет в список сообщений для чата на стороне клиента,
        заменяет последнее сообщение в чате с пользователем на новое
        """
        if self.selected_chat_id != '':
            msg = self.client.sendmessage(self.selected_chat_id, message)
            self.add_message(message, from_me=True)
            
            self.change_chat_last_message(msg, self.selected_chat_id)
    
    def change_chat_last_message(self, message: MessageModel, chat_id):
        """
        Если найден контакт, обновляет у него последнее сообщение и переводит вверх списка контактов в contacts_viewset
        """
        contact = self.find_contact_by_chat_id(chat_id)
        if contact:
            contact.last_message = message
            old_contact = self.find_contact_view_by_chat_id(chat_id)
            new_contact = asdict(createChatView(contact))
            self.contacts_viewset.remove(old_contact)
            self.contacts_viewset.insert(0, new_contact)
            self.display_viewset.remove(old_contact)
            self.display_viewset.insert(0, new_contact)

    def change_avatar(self, path_to_image):
        self.client.change_avatar(path_to_image)
        self.self_user = None
        self.self_user = self.get_self_user()
        self.current_avatar_url = self.self_user.avatar_url

    def get_user(self, user_id) -> Union[UserModel, None]:
        try:
            user = self.client.getuser(str(user_id))
        except (ServerError, AccessError):
            print("Не удалось найти пользователя")
        else:
            return user
    
    def change_user_data(self, data: dict):
        display_name_changed = data.get("display_name")
        status_changed = data.get("status")
        try:
            self.client.change_user_data(data)
        except (ServerError, AccessError):
            print("Не удалось обновить информацию")
        else:
            if display_name_changed:
                self.current_display_name = display_name_changed
            if status_changed:
                self.current_status = status_changed
