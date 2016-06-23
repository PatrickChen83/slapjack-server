import socket
from time import sleep
import os

socket_path = "/tmp/slapjack.pyserver"
server = None
callback = None

def clear_socket_path():
    global socket_path
    if os.path.exists(socket_path):
        os.remove(socket_path)

def start(path = socket_path):
    global server
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)

    server.listen(1)

def n_time_generator(n):
    def ret(data):
        if n < 0:
            yield False
        else:
            for x in range(n):
                yield True
            yield False
    return ret

one_time = n_time_generator(1)

def listen(stopFunc = n_time_generator(2)):
    global server, callback
    # stopFunc should return a generator that:
    #    yield True if the data is None (only happening on first run)
    #    yield True if the data indicates continuing this connection
    #    yield False if the data indicates closing this connection

    if server is None:
        print("call 'start([path], [callback])' first!")
        return

    data = None
    for isStop in stopFunc(data):
        if not isStop:
            return
        print("Listen for client")
        server.listen(1)

        conn, addr = server.accept()
        print("Accept client")

        while True:
            # This is a blocking read.
            # If recv() return None, the connection is closed.

            # Note that the length of each message < 20

            data = conn.recv(20)
            if not data:
                print("Connection closed by client")
                conn.close();
                break
            if callback:
                callback(conn, data)

def send(conn, data):
    conn.sendall(data)

if __name__ == '__main__':
    print("Directly invoke this script. Start testing")
    clear_socket_path()
    callback = send
    start()
    listen()