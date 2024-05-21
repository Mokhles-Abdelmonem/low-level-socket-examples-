import socket


def run_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        try:
            while True:
                message = input("Enter message to send (type 'exit' to close): ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Received from server: {response}")
        except ConnectionResetError:
            print("Connection lost.")
        except KeyboardInterrupt:
            print("Client closing.")

        print("Client closed.")


if __name__ == "__main__":
    run_client()
