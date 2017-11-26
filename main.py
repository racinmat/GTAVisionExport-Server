import json
import queue
import socket
import threading
import time

import os
from flask import Flask, request, jsonify
from flask_cors import CORS


class ThreadedSocket:

    def __init__(self):
        super().__init__()
        self.port = 5555

    def start(self):
        # threading.Thread(target=self.start_socket_server, name='socket_server').start()
        threading.Thread(target=self.start_socket_client, name='socket_server').start()
    #
    # def start_socket_server(self):
    #     s = socket.socket()
    #     # host = '0.0.0.0'
    #     host = 'localhost'
    #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     s.bind((host, self.port))
    #
    #     s.listen()
    #     client, addr = s.accept()
    #     print("established socket connection")
    #     while True:
    #         message = q.get()
    #         print("taken from queue: ", message)
    #         client.send(message.encode('utf-8'))
    #         q.task_done()
    #         if message == "GET_SCREEN":
    #             # wait for response
    #             data = client.recv(1024).decode('utf-8')
    #             print("got data: {}".format(data))
    #             data = client.recv(1024).decode('utf-8')
    #             print("got data: {}".format(data))

    def wait_to_connect(self, s, host):
        connected = False
        while not connected:
            print("waiting for connection to server")
            try:
                s.connect((host, self.port))
                connected = True
                print("connected")
            except ConnectionRefusedError as e:
                time.sleep(5)

    def start_socket_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        print(host)
        self.wait_to_connect(s, host)

        print("connected to socket server")
        while True:
            message = q.get()
            if type(message) is tuple:
                message, params = message
            print("taken from queue: ", message)
            s.sendall(message.encode('utf-8'))
            # if message == 'SET_TIME':
            #     send_params = s.recv(1024).decode('utf-8')
            #     if send_params != 'SEND_PARAMS':
            #         raise Exception("Some shit happened. Data not arrived correctly.")
            #     print("receied: " + send_params)
            #     data_len = str(len(params.encode('utf-8')))
            #     print("data_len: ", data_len)
            #     s.sendall(data_len.encode('utf-8'))
            #     data_len_check = s.recv(1024).decode('utf-8')
            #     if data_len != data_len_check:
            #         raise Exception("Some shit happened. Data not arrived correctly.")
            #     print("params: ", params)
            #     s.sendall(params.encode('utf-8'))

            q.task_done()
            # if message == "GET_SCREEN":
            #     # wait for response
            #     data_len = s.recv(1024)
            #     # according to https://stackoverflow.com/questions/13514614/why-is-network-byte-order-defined-to-be-big-endian
            #     # network byte order is high endian
            #     data_len_int = int.from_bytes(data_len, byteorder='big')
            #     print("got data last: size: {}".format(data_len_int))
            #     data = s.recv(data_len_int)
            #     with open('./last_screen.bin', 'wb+') as file:
            #         file.write(data)
            #         print("saved bytes to file")


def test_queue():
    q.put('hello')
    time.sleep(1)
    q.put('world')
    time.sleep(1)
    q.put('i work')
    time.sleep(1)
    q.put('fuck yeah!')


def main():
    # use_web_server = False
    use_web_server = True
    ThreadedSocket().start()
    if use_web_server:
        app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        q.put(json.dumps({'name': 'START_SESSION'}))
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
    q.put(json.dumps({'name': data['command']}))
    return '', 200


@app.route('/command/time', methods=['POST'])
def add_time_command():
    data = request.get_json()
    data['command'] = 'SET_TIME'
    print("sent from API: ", data['command'])
    q.put(json.dumps({'name': data['command'], 'time': data['time']}))
    return '', 200


@app.route('/commands', methods=['GET'])
def commands():
    return 'send commands here by post', 200


@app.route('/gallery/count', methods=['GET'])
def gallery_count():
    return str(len(os.listdir(images_dir))), 200


@app.route('/gallery/list', methods=['GET'])
def gallery_list():
    # files = list(os.listdir(images_dir))
    files = list([os.path.join('img', i) for i in os.listdir(images_dir)])
    return json.dumps(files), 200


if __name__ == '__main__':
    q = queue.Queue(0)
    # images_dir = 'D:\\GTAV_extraction_output\\rgb-jpeg'
    images_dir = 'D:\\projekty\\GTA-V-extractors\\output\\rgb-jpeg'
    main()

