import requests
from random import randint

data = {'username': "".join([str(randint(0, 1000)) for i in range(10)]), 'password': 'qweqweqwe123'}

requests.post("http://127.0.0.1:8000/api/v1/auth/users/", json=data)
token = requests.post("http://127.0.0.1:8000/api/v1/auth/token/login", json=data)

token = token.json()['auth_token']
print(token)

headers = {'Authorization': f'Token {token}'}

url = "http://127.0.0.1:8000/api/v1/chat"
data = {
    'users': [2],
}

r = requests.post(url=url, headers=headers, data=data)
print(r.text)