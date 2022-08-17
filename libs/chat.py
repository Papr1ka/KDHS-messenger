from datetime import datetime
from libs.message import Message
from typing import List, Union


class Chat():
    
    id: int
    created_at: datetime
    destination_username: str
    destination_id: int
    last_message: Union[Message, None]
    messages: List[int]

    def from_data(self, data: dict):
        self.id = data['id']
        self.messages = data['messages']
        self.created_at = datetime.fromisoformat(data['created_at'][:-1]+ "+00:00")
        self.destination_username = data['users'][0]['username']
        self.destination_id = data['users'][0]['id']
        self.last_message = None if data['last_message'] == [] else Message().from_data(data['last_message'][0])
        return self
