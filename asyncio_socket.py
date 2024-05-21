import asyncio

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

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = TCPServer()
    asyncio.run(server.start_server())
