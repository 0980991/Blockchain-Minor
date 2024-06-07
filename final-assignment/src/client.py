import socket
import pickle
import asyncio

class ClientRequest:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def to_bytes(self):
        return pickle.dumps({'type': self.type, 'data': self.data})

async def send_data(type, data):
    host, port = 'localhost', 5005
    request = ClientRequest(type=type, data=data)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(request.to_bytes())
            response = pickle.loads(sock.recv(4096))
            return response
    except ConnectionRefusedError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

