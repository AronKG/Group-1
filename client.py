import asyncio
import websockets
import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WebSocket Client')
    parser.add_argument('host', type=str, help='hostname or IP address of the server')
    parser.add_argument('port', type=int, help='port number of the server')
    args = parser.parse_args()
    client = Client(args.host, args.port)
    asyncio.get_event_loop().run_until_complete(client.start_chat())
