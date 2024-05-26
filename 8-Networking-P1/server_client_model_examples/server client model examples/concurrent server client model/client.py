import socket

HOST = socket.gethostbyname('localhost')
PORT = 5050        # Arbitrary non-privileged port

ADDR = (HOST, PORT)
HEADER_SIZE = 64
DATA_FORMAT = 'utf-8'
DIS_MES = '!END'
RET_MES = 'Server received your message!'
DEF_BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(ADDR)
    sending_flag = True
except OSError as message:
    client_socket.close()
    sending_flag = False

def send_data(message):
    formatted_message = message.encode(DATA_FORMAT)
    msg_len = len(formatted_message)
    message_header = str(msg_len).encode(DATA_FORMAT)
    message_header += b' ' * (HEADER_SIZE - len(message_header))  #fill in header to 64 bytes so server understands.

    #send header and message
    client_socket.send(message_header)
    client_socket.send(formatted_message)

    recv_mes = client_socket.recv(DEF_BUFFER_SIZE).decode(DATA_FORMAT)
    print(recv_mes)

while sending_flag:
    print("you can now send a message")
    print("to terminate the connection enter a blank message please")
    message = input("Write your message please: ")
    if message:
        send_data(message)
    else:
        send_data(DIS_MES)
        sending_flag = False

client_socket.close()