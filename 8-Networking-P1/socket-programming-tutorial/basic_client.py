import socket

HOST="127.0.0.1"
HOST = socket.gethostbyname('localhost')
PORT=6968


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello Maurice")
    data = s.recv(1024)

print(f"Received data: {data!r}")
