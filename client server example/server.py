import selectors
import socket
import types
import pickle

selector = selectors.DefaultSelector()
numbers = []

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f'Accepted connection from {addr}')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            message = pickle.loads(recv_data)
            handle_request(message)
            data.outb += pickle.dumps('Success')
        else:
            print(f'Closing connection to {data.addr}')
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def handle_request(message):
    global numbers
    try:
        request = message  # Using the unpickled data directly
        if request['type'] == 'addNumber':
            numbers.append(request['data'])
        elif request['type'] == 'removeNumber':
            numbers.remove(request['data'])
        print(f'Current numbers: {numbers}')
    except Exception as e:
        print(f'Error handling request: {e}')

def start_server(host='localhost', port=65432):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f'Listening on {(host, port)}')
    lsock.setblocking(False)
    selector.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        selector.close()

# Start the server
if __name__ == "__main__":
    start_server()
