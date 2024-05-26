import socket

HOST = socket.gethostbyname('localhost')  # Assuming the server is running on the same machine
PORT = 5050         # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received:', str(data, 'utf-8'))
