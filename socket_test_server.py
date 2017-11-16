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
        if data == "GET_SCREEN":
            client.send("size in bytes".encode('utf-8'))
            client.send("last".encode('utf-8'))
        elif data == "SET_TIME":
            data_size = int(client.recv(1024).decode('utf-8'))
            client.sendall(str(data_size).encode('utf-8'))
            print("RECEIVED PARAMS LEN: ", data_size)
            params = client.recv(data_size).decode('utf-8')
            print("RECEIVED PARAMS: ", params)
