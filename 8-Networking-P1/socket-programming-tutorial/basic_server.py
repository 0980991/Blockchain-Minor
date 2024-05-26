import socket
import threading

HOST="127.0.0.1"
PORT=6968



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Client: {addr} connected to the server")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
