#server example
import socket

if __name__ == '__main__':
    s = socket.socket()
    # host = '0.0.0.0'
    host = 'localhost'
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, 5555))
    s.listen()
    client, addr = s.accept()
    print("established socket connection")
    while True:
        data = client.recv(1024).decode('utf-8')
        print("RECEIVED: ", data)
