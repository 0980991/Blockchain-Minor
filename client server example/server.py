import selectors
import socket
import types
import pickle

selector = selectors.DefaultSelector()
data = []

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
            response = handle_request(message)
            data.outb += pickle.dumps(response)
        else:
            print(f'Closing connection to {data.addr}')
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def handle_request(message):
    global data
    try:
        request = message  # Using the unpickled data directly
        if request['type'] == 'add':
            data.append(request['data'])
            print(f'Current data: {data}')
            return 'Success'
        elif request['type'] == 'remove':
            data.remove(request['data'])
            print(f'Current data: {data}')
            return 'Success'
        else:
            print(f'type {request["type"]} is not recognized')
            print(f'Current data: {data}')
            return f'Failed: type {request["type"]} is not recognized'
        
    except Exception as e:
        print(f'Error handling request: {e}')
        return f'Failed: {str(e)}'

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
