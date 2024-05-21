import socket
from concurrent.futures import ThreadPoolExecutor

class TCPServer:
    def __init__(self, host='127.0.0.1', port=65432, max_workers=100):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def handle_client(self, client_socket, client_address):
        print(f"Connection from {client_address} has been established.")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received from {client_address}: {message}")
                client_socket.sendall(f"Echo: {message}".encode('utf-8'))
            except ConnectionResetError:
                print(f"Connection with {client_address} lost.")
                break
        client_socket.close()
        print(f"Connection with {client_address} closed.")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.executor.submit(self.handle_client, client_socket, client_address)

if __name__ == "__main__":
    server = TCPServer(max_workers=100)
    server.start()
