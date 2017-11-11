#client example
import socket

if __name__ == '__main__':
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = socket.socket()
    host = 'localhost'
    # host = '127.0.0.1'
    # host = socket.gethostname()
    print(host)
    client_socket.connect((host, 5555))
    # client_socket.send(b'hello')
    while True:
        data = client_socket.recv(512).decode('utf-8')
        print("RECEIVED: ", data)
