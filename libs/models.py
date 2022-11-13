from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Union
from settings import SERVER_URL


@dataclass
class UserModel:
    id: int
    username: str
    date_joined: str
    avatar_image: str
    status: str
    display_name: str

def createUser(data: dict) -> UserModel:
    user = UserModel(
        id=data['id'],
        username=data['user']['username'],
        date_joined=datetime.fromisoformat(data['user']['date_joined'][:-1]+ "+00:00").astimezone(),
        avatar_image=SERVER_URL + data['avatar_image'] if data['avatar_image'] else "assets/icons/user.png",
        status=data['status'],
        display_name=data['display_name']        
    )
    return user


@dataclass
class MessageModel():
    
    id: int
    author_id: str
    created_at: datetime
    text: str
    chat_id: int
    
def createMessage(data: dict) -> MessageModel:
    message = MessageModel(
        id=data['id'],
        author_id=data['author_id'],
        created_at=datetime.fromisoformat(data['created_at'][:-1]+ "+00:00").astimezone(),
        text=data['text'],
        chat_id=data['chat'],    
    )
    return message


@dataclass
class ChatAPIModel():
    id: int
    messages: List[int]
    created_at: datetime
    users: List[int]

def createChatAPI(data: dict) -> ChatAPIModel:
    chat = ChatAPIModel(
        id=data['id'],
        messages=data['messages'],
        created_at=datetime.fromisoformat(data['created_at'][:-1]+ "+00:00").astimezone(),
        users=data['users']
    )
    return chat


@dataclass
class ChatModel(ChatAPIModel):
    destination_username: str
    destination_id: int
    last_message: Union[MessageModel, None]
    avatar_url: str

def createChat(data: dict):
    chat = ChatModel(
        id=data['id'],
        created_at=datetime.fromisoformat(data['created_at'][:-1]+ "+00:00").astimezone() if not isinstance(data['created_at'], datetime) else data['created_at'],
        destination_username=data['users'][0]['username'],
        destination_id=data['users'][0]['id'],
        last_message=None if data['last_message'] == [] else createMessage(data['last_message'][0]),
        messages=data['messages'],
        avatar_url=SERVER_URL + data['users'][0]['avatar_image'] if data['users'][0]['avatar_image'] else "assets/icons/user.png",
        users=[i['id'] for i in data['users']]
    )
    return chat



@dataclass
class ContactViewModel():
    id: str
    text: str
    secondary_text: str
    time: datetime
    image: str

@dataclass
class ChatViewModel(ContactViewModel):
    unread_messages: bool
    chat_id: str


def createContact(user: UserModel):
    contact_view = ContactViewModel(
        id=str(user.id),
        text=user.username,
        secondary_text='Написать первым',
        time='',
        image=user.avatar_image
    )
    return contact_view


def createChatView(chat: ChatModel):
    chat_view = ChatViewModel(
        id=str(chat.id),
        text=chat.destination_username,
        unread_messages=True,
        secondary_text='Написать первым' if not chat.last_message else chat.last_message.text,
        time='' if not chat.last_message else chat.last_message.created_at.strftime("%H:%M"),
        chat_id=str(chat.id),
        image=chat.avatar_url
    )
    return chat_view

def createChatViewFromKeys(data: dict):
    chat_view = ChatViewModel(
        id=str(data['id']),
        text=data['destination_username'],
        unread_messages=True,
        secondary_text='Написать первым' if not data['last_message'] else data['last_message'].text,
        time='' if not data['last_message'] else data['last_message'].created_at.strftime("%H:%M"),
        chat_id=str(data['id']),
        image=data['avatar_url']
    )
    return chat_view
