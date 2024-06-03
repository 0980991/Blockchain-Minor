import socket
import pickle
from enum import Enum

class RequestType(Enum):
    ADD_NUMBER = 'addNumber'
    REMOVE_NUMBER = 'removeNumber'

class ClientRequest:
    def __init__(self, type, data):
        # Attempt to convert the type to RequestType, if it's a string.
        if isinstance(type, str):
            try:
                type = RequestType(type)
            except ValueError:
                raise ValueError(f'Invalid request type: {type}. Must be "addNumber" or "removeNumber".')

        if not isinstance(type, RequestType):
            raise ValueError(f'type must be an instance of RequestType Enum, got {type}')

        try:
            data = int(data)
        except ValueError:
            raise ValueError(f'data must be an integer, got {data}')

        self.type = type
        self.data = data

    def to_bytes(self):
        return pickle.dumps({'type': self.type.value, 'data': self.data})

def send_data(type, data):
    host, port = 'localhost', 65432
    request = ClientRequest(type=type, data=data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(request.to_bytes())
        response = pickle.loads(sock.recv(1024))
        print('Received', repr(response))

# Example usage
if __name__ == "__main__":
    while True:
        try:
            type_input = input('Please give the type (addNumber/removeNumber):\n')
            data_input = input('Please give the data (integer):\n')
            send_data(type=type_input, data=data_input)
        except ValueError as e:
            print(e)
