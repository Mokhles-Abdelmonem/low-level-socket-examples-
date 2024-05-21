import socket
from locust import User, TaskSet, task, between, events
import time


class TCPSocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send(self, message):
        self.client_socket.sendall(message.encode('utf-8'))

    def receive(self):
        return self.client_socket.recv(1024).decode('utf-8')

    def close(self):
        self.client_socket.close()


class TCPClientTaskSet(TaskSet):


    def on_start(self):
        self.socket_client = TCPSocketClient("localhost", 65432)
        self.socket_client.connect()

    def on_stop(self):
        self.socket_client.close()

    @task
    def send_and_receive(self):
        start_time = time.time()
        try:
            self.socket_client.send("Hello, server!")
            response = self.socket_client.receive()
            total_time = int((time.time() - start_time) * 1000)
            if response:
                events.request.fire(
                    request_type="tcp",
                    name="send_and_receive",
                    response_time=total_time,
                    response_length=len(response),
                )
            else:
                events.request.fire(
                    request_type="tcp",
                    name="send_and_receive",
                    response_time=total_time,
                    exception=Exception("No response received"),
                )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="tcp",
                name="send_and_receive",
                response_time=total_time,
                exception=e,
            )

class TCPClientTaskSet1(TCPClientTaskSet):
    def on_start(self):
        self.socket_client = TCPSocketClient("localhost", 65432)
        self.socket_client.connect()


class TCPClientTaskSet2(TCPClientTaskSet):
    def on_start(self):
        self.socket_client = TCPSocketClient("localhost", 65433)
        self.socket_client.connect()


class TCPClientTaskSet3(TCPClientTaskSet):
    def on_start(self):
        self.socket_client = TCPSocketClient("localhost", 65433)
        self.socket_client.connect()


class TCPClientTaskSet4(TCPClientTaskSet):
    def on_start(self):
        self.socket_client = TCPSocketClient("localhost", 65434)
        self.socket_client.connect()


class TCPUser(User):
    tasks = [TCPClientTaskSet1, TCPClientTaskSet2, TCPClientTaskSet3, TCPClientTaskSet4]
    wait_time = between(1, 2)
    host = "127.0.0.1"
    port = 65432
