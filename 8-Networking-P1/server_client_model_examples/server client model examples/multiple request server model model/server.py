import socket

HOST = socket.gethostbyname('localhost')
PORT = 5050        # Arbitrary non-privileged port

ADDR = (HOST, PORT)
HEADER_SIZE = 64
DATA_FORMAT = 'utf-8'
DIS_MES = '!END'
RET_MES = 'Server received your message!'

def handle_client(conn, addr):
    print('Connected by', addr)

    connected_flag = True
    while connected_flag:
        data_length = conn.recv(HEADER_SIZE).decode(DATA_FORMAT)
        if data_length:
            data_length = int(data_length)
            data = conn.recv(data_length).decode(DATA_FORMAT)
            if data == DIS_MES:
                connected_flag = False
            print(f"received data from {addr}: {data}")
            conn.send(RET_MES.encode(DATA_FORMAT))
 
    conn.close()


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDR)
        while True:
            s.listen(1)
            print('Server listening on', ADDR)
            conn, addr = s.accept()
            print("a connection has been made...")
            handle_client(conn, addr)

start()