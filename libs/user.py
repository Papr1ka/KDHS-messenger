from datetime import datetime
from libs.server import SERVER_URL


class User():
    
    id: int
    username: str
    avatar_url: str
    
    def from_data(self, data: dict):
        self.id = data['id']
        self.username = data['user']['username']
        self.avatar_url = SERVER_URL + data['avatar_image'] if data['avatar_image'] else "assets/icons/user.png"
        return self
