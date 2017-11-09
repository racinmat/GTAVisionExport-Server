import queue
import socket
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS


class ThreadedSocketServer:

    def __init__(self):
        super().__init__()
        self.port = 5555

    def start(self):
        threading.Thread(target=self.start_socket, name='socket_server').start()

    def start_socket(self):
        s = socket.socket()
        host = socket.gethostname()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, self.port))

        s.listen()
        client, addr = s.accept()
        print("connection established")
        while True:
            message = q.get()
            client.send(message)
            print(message)
            q.task_done()


def test_queue():
    q.put('hello')
    time.sleep(1)
    q.put('world')
    time.sleep(1)
    q.put('i work')
    time.sleep(1)
    q.put('fuck yeah!')


def main():
    ThreadedSocketServer().start()
    app.run(debug=True, host='localhost', port=5000)
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
    print(data['command'])
    q.put(data['command'])
    return '', 200


@app.route('/commands', methods=['GET'])
def commands():
    return 'send commands here by post', 200


if __name__ == '__main__':
    q = queue.Queue()
    main()

