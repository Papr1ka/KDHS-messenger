from datetime import datetime
from libs.server import SERVER_URL


class User():
    
    id: int
    username: str
    avatar_url: str
    date_created: datetime
    
    def from_data(self, data: dict):
        self.id = data['id']
        self.username = data['user']['username']
        self.date_created = datetime.fromisoformat(data['user']['date_joined'][:-1]+ "+00:00").astimezone()
        self.avatar_url = SERVER_URL + data['avatar_image'] if data['avatar_image'] else "assets/icons/user.png"
        return self
