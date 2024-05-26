import socket
import threading

HOST="127.0.0.1"
PORT=6968

ADDR = (HOST, PORT)
HEADER_SIZE = 64
DATA_FORMAT = 'utf-8'
DIS_MES = '!END'
RET_MES = 'Server received your message!'

def handle_client(conn, addr):
    print(f"New Connection: {addr}")
    print(f"Current active connections: {threading.active_count()}")

    is_connected = True
    while is_connected:
        data_length = conn.recv(HEADER_SIZE).decode(DATA_FORMAT)
        if data_length:
            print(f"Data length = {type(data_length)} : {data_length}")
            data_length = int(data_length)
            data = conn.recv(data_length).decode(DATA_FORMAT)
            if data == DIS_MES:
                is_connected = False
            print(f"Received data: {data} from {addr}")
            conn.send(RET_MES.encode(DATA_FORMAT))

    conn.close()

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening on", ADDR)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print("A connection was succesfully made!")

start()