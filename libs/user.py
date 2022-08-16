from datetime import datetime


class User():
    
    id: int = -1
    username: str = ""
    #date_joined: datetime
    
    def from_data(self, data: dict):
        self.id = data['id']
        self.username = data['username']
        #self.date_joined = datetime.fromisoformat(data['user']['date_joined'][:-1]+ "+00:00")
