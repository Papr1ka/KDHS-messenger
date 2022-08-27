from datetime import datetime


class Message():
    
    id: int
    author_id: str
    created_at: datetime
    text: str
    chat_id: int
    
    def from_data(self, data: dict):
        self.id = data['id']
        self.author_id = data['author_id']
        self.created_at = datetime.fromisoformat(data['created_at'][:-1]+ "+00:00").astimezone()
        self.text = data['text']
        self.chat_id = data['chat']
        return self
