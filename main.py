import queue
import socket
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS


class ThreadedSocket:

    def __init__(self):
        super().__init__()
        self.port = 5555

    def start(self):
        # threading.Thread(target=self.start_socket_server, name='socket_server').start()
        threading.Thread(target=self.start_socket_client, name='socket_server').start()

    def start_socket_server(self):
        s = socket.socket()
        # host = '0.0.0.0'
        host = 'localhost'
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, self.port))

        s.listen()
        client, addr = s.accept()
        print("established socket connection")
        while True:
            message = q.get()
            print("taken from queue: ", message)
            client.send(message.encode('utf-8'))
            q.task_done()
            if message == "GET_SCREEN":
                # wait for response
                data = client.recv(1024).decode('utf-8')
                print("got data: {}".format(data))
                data = client.recv(1024).decode('utf-8')
                print("got data: {}".format(data))

    def start_socket_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        print(host)
        s.connect((host, self.port))

        print("connected to socket server")
        while True:
            message = q.get()
            print("taken from queue: ", message)
            s.send(message.encode('utf-8'))
            q.task_done()
            if message == "GET_SCREEN":
                # wait for response
                # data = s.recv(1024).decode('utf-8')
                data = s.recv(1024)
                print("got data: {}".format(data))
                # data = s.recv(1024).decode('utf-8')
                data = s.recv(1024)
                print("got data: {}".format(data))


def test_queue():
    q.put('hello')
    time.sleep(1)
    q.put('world')
    time.sleep(1)
    q.put('i work')
    time.sleep(1)
    q.put('fuck yeah!')


def main():
    ThreadedSocket().start()
    app.run(debug=False, host='0.0.0.0', port=5000)
    # test_queue()
    pass
    # "START_SESSION"
    # "STOP_SESSION"
    # "TOGGLE_AUTODRIVE"
    # "ENTER_VEHICLE"
    # "AUTOSTART"
    # "RELOADGAME"
    # "RELOAD"
    # "GET_SCREEN"


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return 'this is python socket server', 200


@app.route('/commands', methods=['POST'])
def add_command():
    data = request.get_json()
    print("sent from API: ", data['command'])
    q.put(data['command'])
    return '', 200


@app.route('/commands', methods=['GET'])
def commands():
    return 'send commands here by post', 200


if __name__ == '__main__':
    q = queue.Queue(0)
    main()

