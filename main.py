import asyncio
import multiprocessing
import os
import signal
import socket

class TCPServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr} has been established.")
        while True:
            try:
                data = await reader.read(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {addr}: {message}")
                writer.write(f"Echo: {message}".encode('utf-8'))
                await writer.drain()
            except ConnectionResetError:
                print(f"Connection with {addr} lost.")
                break
        writer.close()
        await writer.wait_closed()
        print(f"Connection with {addr} closed.")

    async def start_server(self, worker_number):
        print(f"Starting server on port >>>>>>  {self.port + worker_number}")
        server = await asyncio.start_server(self.handle_client, self.host, self.port + worker_number)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

def run_server(worker_number):
    server = TCPServer()
    asyncio.run(server.start_server(worker_number))

def create_workers(worker_number):
    workers = []
    for w in range(worker_number):
        worker = multiprocessing.Process(target=run_server, args=(w,))
        worker.start()
        workers.append(worker)
    return workers


def stop_workers(workers):
    for worker in workers:
        worker.terminate()
        worker.join()


if __name__ == "__main__":
    num_workers = os.cpu_count()
    workers = create_workers(num_workers)

    def graceful_shutdown(signum, frame):
        print("Shutting down...")
        stop_workers(workers)
        exit(0)

    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    # Keep the main process running
    while True:
        signal.pause()
