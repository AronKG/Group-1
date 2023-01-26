import asyncio
import websockets

class Client:
    
    def __init__(self,host,port=3000):
        self.host = host;
        self.port = port;
        self.uri = f"ws://{self.host}:{self.port}"
        
    async def start_chat(self):
        async with websockets.connect(self.uri) as websocket:
            while True:
                message = input('Enter your message: ')
                await websocket.send(message)
                print(f'Sent: {message}')
                response = await websocket.recv()
                print(f'Received: {response}')

client = Client(host="192.168.1.4")
asyncio.get_event_loop().run_until_complete(client.start_chat())
