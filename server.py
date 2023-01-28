import asyncio
import websockets

class Server:
    clients = set()

    def __init__(self,ip="localhost",port=3000):
        self.ip = ip;
        self.port = port;
        
    async def register(self,websocket):
        self.clients.add(websocket)
        print(f'{websocket} connected')

    async def unregister(self,websocket):
        self.clients.remove(websocket)
        print(f'{websocket} disconnected')

    async def broadcast(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def chat_handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.broadcast(message)
        finally:
            await self.unregister(websocket)

    def start_server(self):
        print(f"Server running on {self.ip} on port {self.port}")
        start_server = websockets.serve(self.chat_handler, self.ip, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

server = Server(ip="192.168.1.4")
server.start_server()
