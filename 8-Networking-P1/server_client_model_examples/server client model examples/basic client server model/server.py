import socket

HOST = socket.gethostbyname('localhost')
PORT = 5050        # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Server listening on', (HOST, PORT))
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received:', str(data, 'utf-8'))
            conn.sendall(data)
