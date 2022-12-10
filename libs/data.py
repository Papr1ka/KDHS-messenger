from functools import partial
from libs.exceptions import AccessError, InvalidDisplayNameError, InvalidStatusError, ServerError, NotAutirizedError
from requests.exceptions import RequestException
from libs.models import *
from libs.snackcontroller import Controller
from libs.server import Client
from libs.utils.window import get_window_type
from libs.components.snackbar import show_error_snackbar, show_success_snackbar
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivymd.app import MDApp
from logging import Logger
from libs.notify import notify

BaseExceptions = (ServerError, AccessError, RequestException, NotAutirizedError)

class Data():
    
    client: Client
    controller: Controller
    app: MDApp
    self_user: UserModel = None
    Logger: Logger = None

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

    def on_login(self):
        print("on_login")
        try:
            self.self_user = self.get_self_user()
        except BaseExceptions:
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
        self.current_username = self.self_user.username
        self.current_avatar_url = self.self_user.avatar_image
        print(self.self_user.date_joined)
        self.current_date_created = self.self_user.date_joined.strftime("%d:%m:%Y")
        self.current_display_name = self.self_user.display_name
        self.current_status = self.self_user.status
        self.load_contacts()
        self.show_contacts()
        self.app = MDApp.get_running_app()

    def login(self, username, password):
        try:
            self.client.autorize(username, password)
        except (ServerError, RequestException):
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
            return False
        return True

    def register(self, username, password):
        try:
            self.client.register(username, password)
        except (ServerError, RequestException):
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
            return False
        return True

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
        except BaseExceptions:
            self.display_viewset.clear()
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
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
        except BaseExceptions:
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
        else:
            try:
                user = self.client.getuser(str(user_id))
            except BaseExceptions:
                self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
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
        except BaseExceptions:
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
        except Exception as E:
            self.controller.show(partial(show_error_snackbar, "Ошибка"), 2)
        else:
            self.contacts.clear()
            for chat in data:
                chat_model = createChat(chat)
                self.contacts.append(chat_model)
                self.contacts_viewset.append(asdict(createChatView(chat_model)))
    
    def post_load_contacts(self, size: int):
        try:
            data = self.client.getcontacts(size)['chats']['chats']
        except BaseExceptions:
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
        except Exception as E:
            self.controller.show(partial(show_error_snackbar, "Ошибка"), 2)
        else:
            for chat in data:
                chat_model = createChat(chat)
                self.contacts.insert(0, (chat_model))
                self.contacts_viewset.insert(0, asdict(createChatView(chat_model)))
    
    def get_messages(self, chat_id: str):
        """
        Получает список сообщений для чата с id - chat_id, если история сообщений существует, загружает с неё, если нет - с сервера
        """
        story_exists = self.chats.get(chat_id, None)
        if not story_exists:
            try:
                messages = self.client.getmessagelist(chat_id, '1')
            except BaseExceptions:
                messages = []
                self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
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
        
        data = self.generate_message_view(content, from_me)
        
        self.messages.append(data)
        self.story_message(data)
    
    def generate_message_view(self, content: str, from_me=True):
        """
        Возвращает словарь для представления сообщения
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
        return data
    
    def story_message(self, data: dict, chat_id=None):
        """
        Добавляет данные для отображения сообщения в конкретный чат
        """
        current_chat_id = chat_id if chat_id is not None else self.selected_chat_id
        if current_chat_id != '':
            story_exists = self.chats.get(current_chat_id, None)
            if not story_exists:
                self.chats[current_chat_id] = []
            self.chats[current_chat_id].append(data)
    
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
    
    def on_message(self, message: MessageModel):
        """
        Получает входящие сообщения в лайв режиме
        """
        if str(message.chat_id) == self.selected_chat_id:
            self.add_message(message.text, from_me=False)
        else:
            data = self.generate_message_view(message.text, from_me=False)
            self.story_message(data, str(message.chat_id))
            notify(self.find_contact_by_chat_id(str(message.chat_id)).destination_username, message.text)
        self.change_chat_last_message(message, str(message.chat_id))
            
    
    def check_new_chats(self, data: dict):
        """
        сюда приходит обновлённый пользотель (наш пользователь) (мы)
        если есть новые чаты, возвращаем true
        """
        print("я не хочу эту поеботу обрабатывать", data)
        user = self.get_self_user()
        if data.get('data'):
            data = data['data']
        
        if data['chats']:
            new_chat_length = len(data['chats'])
            old_chat_length = len(user.chats)
            if new_chat_length > old_chat_length:
                for i in range(new_chat_length - 1, old_chat_length - 1, -1):
                    self.self_user.chats.append(data['chats'][i]['id'])
                self.post_load_contacts(new_chat_length - old_chat_length)
                self.show_contacts()
                return True
        return False
                

    def change_avatar(self, path_to_image):
        self.client.change_avatar(path_to_image)
        self.self_user = None
        self.self_user = self.get_self_user()
        self.current_avatar_url = self.self_user.avatar_url

    def get_user(self, user_id) -> Union[UserModel, None]:
        try:
            user = self.client.getuser(str(user_id))
        except BaseExceptions:
            self.controller.show(partial(show_error_snackbar, "Ошибка Сервера, попробуйте позже"), 2)
        else:
            return user
    
    def change_user_data(self, data: dict):
        display_name_changed = data.get("display_name")
        status_changed = data.get("status")
        try:
            self.client.change_user_data(data)
        except BaseExceptions:
            self.controller.show(partial(show_error_snackbar, "Не удалось обновить информацию"), 2)
        else:
            if display_name_changed:
                self.current_display_name = display_name_changed
            if status_changed:
                self.current_status = status_changed
