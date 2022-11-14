import asyncio
from libs.server import WebsocketClient


w = WebsocketClient()
w.autorize("root", "123")
asyncio.run(w.connect())
asyncio.run(w.listen())
