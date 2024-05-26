import socket
import threading
import random

HOST="127.0.0.1"
PORT=6968

ADDR = (HOST, PORT)
HEADER_SIZE = 64
DATA_FORMAT = 'utf-8'
DIS_MES = '!END'
RET_MES = 'Server received your message!'

USERS = []

def handle_client(conn, addr):
    if addr not in USERS:
        username = input("Enter your username")
        if not username:
            username = f"Guest {random.randint(1, 999999)}"
    else:
        username = get_username_by_addr(addr)
    print(f"New Connection: {username}")
    print(f"Current active connections: {threading.active_count()}")

    is_connected = True
    while is_connected:
        print("HELLO FROM LINE 28")
        data_length = conn.recv(HEADER_SIZE).decode(DATA_FORMAT)
        print("HELLO FROM LINE 30")
        if data_length:
            print(f"Data length = {type(data_length)} : {data_length}")
            data_length = int(data_length)
            data = conn.recv(data_length).decode(DATA_FORMAT)
            if data == DIS_MES:
                is_connected = False
            print(f"{username}: {data}")
            conn.send(RET_MES.encode(DATA_FORMAT))

    conn.close()

def get_username_by_addr(addr, user_list):
    for item in user_list:
        if item[0] == addr:
            return item[1]
    return None  # Return None if no matching address is found

def broadcast(message, current_conn):
    for client in clients:
        if client != current_conn:
            try:
                client.send(message.encode(DATA_FORMAT))
            except:
                remove_client(client)
                
def remove_client(conn):
    if conn in clients:
        clients.remove(conn)


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