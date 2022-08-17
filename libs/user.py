from datetime import datetime


class User():
    
    id: int
    username: str
    
    def from_data(self, data: dict):
        self.id = data['id']
        self.username = data['username']
        return self
