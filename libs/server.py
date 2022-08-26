import requests
from libs.exceptions import CommonPasswordError, ServerError, AccessError, ShortPasswordError, UserExistsError, NotAutirizedError
from pathlib import Path
from io import BytesIO

SERVER_URL = "http://127.0.0.1:8000"
#SERVER_URL = "https://connection-net.herokuapp.com"


URL = SERVER_URL + "/api/v1/"

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


class Client():
    def __init__(self) :
        self.autorized = False
    
    
    def requiredAuthorization(func):
        def wrapper(self, *args, **kwargs):
            if not self.autorized:
                raise NotAutirizedError("Required Authorization")
            return func(self, *args, **kwargs)
        return wrapper
            
    @requiredAuthorization
    def getcontacts(self) -> dict:
        url = URL + 'chatList'
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            raise ServerError(f'Server exception 204: {r.text}')
        elif r.status_code == 400:
            raise ServerError(f'Server exception 400: {r.text}')
        raise AccessError(r.text)
    
    
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
            self.headers = {'Authorization': f'Token {self.token}'}
            return self.token
        raise AccessError(r.text)
    
    @requiredAuthorization
    def getMe(self) -> dict:
        url = URL + 'user'
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 204:
            raise ServerError(f'Server exception 204: {r.text}')
        elif r.status_code == 400:
            raise ServerError(f'Server exception 400: {r.text}')
        raise AccessError(r.text)
    
    @requiredAuthorization
    def change_username(self, username: str):
        if not isinstance(username, str):
            raise ValueError("Expected username:str")
        url = URL + 'user'
        data = {
            'username': username
        }
        r = requests.put(url=url, headers=self.headers, data=data)
        if r.status_code == 200:
            result = r.json()
            error = result.get("error", None)
            if error:
                raise ValueError(error)
            return result
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
    def getmessagelist(self, chat_id: str, part: str) -> dict:
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
                raise ValueError(error)
            return result
        raise AccessError(r.text)

    @requiredAuthorization
    def sendmessage(self, chat_id: str, text):
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
            return result
        raise AccessError(r.text)

    @requiredAuthorization
    def createchat(self, user_id: str):
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
            return result
        raise AccessError(r.text)
    
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
