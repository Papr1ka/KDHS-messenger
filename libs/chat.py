from datetime import datetime
from libs.message import Message
from typing import List, Union
from libs.server import SERVER_URL


class Chat():
    
    id: int
    created_at: datetime
    destination_username: str
    destination_id: int
    last_message: Union[Message, None]
    messages: List[int]
    avatar_url: str

    def from_data(self, data: dict):
        self.id = data['id']
        self.messages = data['messages']
        self.created_at = datetime.fromisoformat(data['created_at'][:-1]+ "+00:00")
        self.destination_username = data['users'][0]['username']
        self.destination_id = data['users'][0]['id']
        self.last_message = None if data['last_message'] == [] else Message().from_data(data['last_message'][0])
        self.avatar_url = SERVER_URL + data['users'][0]['avatar_image'] if data['users'][0]['avatar_image'] else "assets/icons/user.png"
        return self
    
    def to_view(self) -> dict:
        if self.last_message:
            print(self.last_message.created_at)
        data = {
            'id': str(self.id),
            'text': self.destination_username,
            'unread_messages': True,
            'secondary_text': 'Написать первым' if not self.last_message else self.last_message.text,
            'time': '' if not self.last_message else self.last_message.created_at.astimezone().strftime("%H:%M"),
            'chat_id': str(self.id),
            'image': self.avatar_url
        }
        return data
