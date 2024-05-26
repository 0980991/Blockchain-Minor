import socket
import threading

HOST="127.0.0.1"
HOST = socket.gethostbyname('localhost')
PORT=6968

ADDR = (HOST, PORT)
HEADER_SIZE = 64
DATA_FORMAT = 'utf-8'
DIS_MES = '!END'
RET_MES = 'Server received your message!'
DEF_BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(ADDR)
    is_sending = True
except OSError as message:
    client_socket.close()
    is_sending = False

    receive_thread = threading.Thread(target=receive_data, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_data, args=(client,))
    send_thread.start()

def receive_data(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break
        
def send_data(message):
    formatted_message = message.encode(DATA_FORMAT)
    msg_len = len(formatted_message)
    message_header = str(msg_len).encode(DATA_FORMAT)
    # fill in header to 64 bytes so server understands.
    message_header += b' ' * (HEADER_SIZE - len(message_header))

    # Send header and message
    client_socket.send(message_header)
    client_socket.send(formatted_message)
    # recv_mes = client_socket.recv(DEF_BUFFER_SIZE).decode(DATA_FORMAT)
    # print(f"Received message: {recv_mes}")


while is_sending:
    message = input("Type your message here: ")
    if message:
        send_data(message)
    else:
        send_data(DIS_MES)
        is_sending = False

client_socket.close()