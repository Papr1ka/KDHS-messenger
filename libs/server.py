import asyncio
import time
import requests
from libs.exceptions import CommonPasswordError, InvalidDisplayNameError, InvalidStatusError, NotFoundError, ServerError, AccessError, ShortPasswordError, UserExistsError, NotAutirizedError
from pathlib import Path
import websockets
import json

from libs.models import ChatAPIModel, ExtendedUserModel, MessageModel, UserModel, createChatAPI, createMessage, createSelfUser, createUser
from settings import SERVER_URL
from libs.websocket import *
from settings import Logger
from libs.utils.behaviors import GetApp
from kivy.clock import Clock


#SERVER_URL = "https://connection-net.herokuapp.com"
name = __name__


URL = SERVER_URL + "/api/v1/"
WS_URL = "ws://" + SERVER_URL[7:] + "/ws/messages/?token="
WS_SERVER_URL = SERVER_URL[7:-5]
PORT = int(SERVER_URL[-4:])
"127.0.0.1/ws/messages/?token=0d2fbbd2e568294cd3b95471388275e300e51a93"

"""
Server Api

userList:
    list of all existing users
    
    GET allowed widh Headers {
        'Authorization': 'Token {str}'
    }
    
    return {
        [
            {
                "id": int,
                "user": {
                    "username": str,
                    "date_joined": timestamp,
                    "id": int
                }
            }
        ]
    }


auth/token/login:

    token authorization

    POST allowed with data {
        'username': str,
        'password': str,
    }

    return {
        'auth_token': str
    }

auth/users/me:

    GET allowed with Headers {
        'Authorization': 'Token {str}'
    }
    
    return {
        "email": str,
        "id": int,
        "username": str
    }

auth/users/:

    POST allowed with data {
        'username': str,
        'password': str
    }

messages:
    #get a part of messages from chat
    GET allowed with Headers {
        'Authorization': 'Token {str}'
    }
    and with data {
        'chat_id': int - chat id
        'part_id': int - index of part of messages 1 - last 20, 2 - last [21-39] !it is counted from last message
    }
    
    return {
        "messages": [
            {
                "id": int,
                "author_id": str,
                "created_at": timestamp,
                "text": str,
                "chat": int
            }
        ]
    }
    # send message to user
    POST allowed with Headers {
        'Authorization': 'Token {str}'
    }
    and with data {
        'chat_id': int
        'text': str
    }

chat:
    # create a chat with user
    POST allowed with Headers {
        'Authorization': 'Token {str}'
    }
    and with data {
        'users': [int] id of the user with whom the chat should be created
    }
    

"""


from kivy.support import install_twisted_reactor
import sys
install_twisted_reactor()
from twisted.internet import reactor




class Client(GetApp):
    
    autorized: bool
    connection: AppWebsocketClientProtocol
    
    def __init__(self) :
        self.autorized = False
        self.connection = None

    def requiredAuthorization(func):
        def wrapper(self, *args, **kwargs):
            if not self.autorized:
                raise NotAutirizedError("Required Authorization")
            return func(self, *args, **kwargs)
        return wrapper
            
    @requiredAuthorization
    def getcontacts(self, size: int = 0) -> dict:
        """
        size: если нужно получить лишь последние несколько контактов
        """
        url = URL + 'chatList'
        if size > 0:
            data = {
                'size': size
            }
            r = requests.get(url=url, headers=self.headers, json=data)
        else:
            r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            raise ServerError(f'Server exception 204: {r.text}')
        elif r.status_code == 400:
            raise ServerError(f'Server exception 400: {r.text}')
        raise AccessError(r.text)
    
    def disconnect(self):
        self.app.reactor_running = False
        reactor.disconnectAll()
        Logger.info(f"{name}: connection stopped")
    
    
    def autorize(self, username: str, password: str) -> str:
        
        if not isinstance(username, str):
            raise ValueError("Expected username:str")
        if not isinstance(password, str):
            raise ValueError("Expected password:str")

        url = URL + 'auth/token/login'
        data = {
            'username': username,
            'password': password
        }
        r = requests.post(url=url, json=data)
        if r.status_code == 200:
            self.token = r.json()['auth_token']
            self.autorized = True
            self.__connect()
            self.headers = {'Authorization': f'Token {self.token}'}
            return self.token
        raise AccessError(r.text)
    
    def __connect(self):
        self.factory = AppWebsocketClientFactory(WS_URL + self.token, self.app)
        reactor.connectTCP(WS_SERVER_URL, PORT, self.factory)
        Logger.info(f"{name}: connection ok")

    @requiredAuthorization
    def getMe(self) -> ExtendedUserModel:
        url = URL + 'user'
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            return createSelfUser(r.json())
        elif r.status_code == 204:
            raise ServerError(f'Server exception 204: {r.text}')
        elif r.status_code == 400:
            raise ServerError(f'Server exception 400: {r.text}')
        raise AccessError(r.text)

    @requiredAuthorization
    def searchUsers(self, username: str) -> list[dict[UserModel]]:
        url = URL + 'user/search'
        r = requests.get(url=url, headers=self.headers, data={'username': username})
        if r.status_code == 200:
            resp = r.json()
            return [createUser(i) for i in resp]
        elif r.status_code == 204:
            raise ServerError(f'Server exception 204: {r.text}')
        elif r.status_code == 400:
            raise ServerError(f'Server exception 400: {r.text}')
        elif r.status_code == 500:
            raise ServerError(f'Server exception 500: Пользователь с таким именем не найден')
        raise AccessError(r.text)

    @requiredAuthorization
    def change_avatar(self, path_to_avatar):
        headers = {'Content-Type': 'multipart/form-data'}
        headers.update(self.headers)
        filename = Path(path_to_avatar).name
        url = URL + 'user'
        data = {
            'avatar': (filename, open(path_to_avatar, 'rb').read(), 'image/jpeg'),
        }
        r = requests.put(url=url, headers=self.headers, files=data)
        if r.status_code == 200:
            result = r.json()
            error = result.get("error", None)
            if error:
                raise ValueError(error)
            return result
        raise AccessError(r.text)

    @requiredAuthorization
    def change_user_data(self, data: dict):
        if not (data.get("display_name") or data.get("status")):
            raise ValueError("Expected display_name or status")
        url = URL + 'user'
        params = {}
        if data.get("display_name"):
            params['display_name'] = data['display_name']
        if data.get("status"):
            params['status'] = data['status']
        
        r = requests.put(url=url, headers=self.headers, data=params)
        result = r.json()
        if r.status_code == 200:
            return result
        elif r.status_code == 400:
            if result.get("error"):
                raise ServerError(result.get("error"))
            if result.get("display_name"):
                raise InvalidDisplayNameError(result.get("display_name"))
            if result.get("status"):
                raise InvalidStatusError(result.get("status"))
        raise AccessError(r.text)

    @requiredAuthorization
    def getuserlist(self) -> dict:
        url = URL + 'userList'
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            raise ServerError(f'Server exception 204: {r.text}')
        elif r.status_code == 400:
            raise ServerError(f'Server exception 400: {r.text}')
        raise AccessError(r.text)
    
    @requiredAuthorization
    def getmessagelist(self, chat_id: str, part: str) -> list[MessageModel]:
        print("request")
        if not isinstance(chat_id, str):
            raise ValueError("Expected chat_id:str")
        if not isinstance(part, str):
            raise ValueError("Expected part:str")
        
        url = URL + 'messages'
        
        data = {
            'chat_id': chat_id,
            'part': part
        }
        
        r = requests.get(url=url, headers=self.headers, json=data)
        if r.status_code == 200:
            result = r.json()
            error = result.get("error", None)
            if error:
                raise ServerError(error)
            resp = []
            for msg in result['messages']:
                resp.append(createMessage(msg))
            return resp
        raise AccessError(r.text)

    @requiredAuthorization
    def sendmessage(self, chat_id: str, text) -> MessageModel:
        if not isinstance(chat_id, str):
            raise ValueError("Expected chat_id:str")

        url = URL + 'messages'
        data = {
            'chat_id': chat_id,
            'text': text
        }
        
        r = requests.post(url=url, headers=self.headers, data=data)
        if r.status_code == 200:
            result = r.json()
            error = result.get("error", None)
            if error:
                raise ValueError(error)
            return createMessage(result)
        raise AccessError(r.text)

    @requiredAuthorization
    def createchat(self, user_id: str) -> ChatAPIModel:
        if not isinstance(user_id, str):
            raise ValueError("Expected user_id:str")

        url = URL + 'chat'
        data = {
            'users': [user_id],
        }
        print(data)
        
        r = requests.post(url=url, headers=self.headers, data=data)
        if r.status_code == 200:
            result = r.json()
            error = result.get("error", None)
            if error:
                raise ValueError(error)
            return createChatAPI(result)
        raise AccessError(r.text)

    @requiredAuthorization
    def getuser(self, user_id: str) -> UserModel:
        if not isinstance(user_id, str):
            raise ValueError("Expected user_id:str")

        url = URL + 'user/' + user_id + "/"
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            return createUser(r.json())
        elif r.status_code == 401:
            raise AccessError(r.text)
        elif r.status_code == 404:
            raise NotFoundError(f"User with id {user_id} does not exists")
        raise ServerError(r.text)
    
    def register(self, username: str, password: str) -> str:
        
        if not isinstance(username, str):
            raise ValueError("Expected username:str")
        if not isinstance(password, str):
            raise ValueError("Expected password:str")

        url = URL + 'auth/users/'
        data = {
            'username': username,
            'password': password
        }
        r = requests.post(url=url, json=data)
        if r.status_code == 201:
            return self.autorize(username=username, password=password)
        elif r.status_code == 400:
            js = r.json()
            if js.get('username', None):
                if js['username'][0] == "A user with that username already exists.":
                    raise UserExistsError(r.text)
            elif js.get('password', None):
                if js['password'][0] == "This password is too short. It must contain at least 8 characters.":
                    raise ShortPasswordError(r.text)
                elif js['password'][0] == "This password is too common.":
                    raise CommonPasswordError(r.text)
            raise AccessError(r.text)
        raise AccessError(r.text)
    
from twisted.python import log
log.startLogging(sys.stdout)