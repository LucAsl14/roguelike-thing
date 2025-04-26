from websockets import ServerConnection
from shared.shared import Message
from server.client import Client
from server.logger import Log
from server.game import Game
import websockets
import traceback
import asyncio

class Server:
    async def run(self):
        self.game = Game(self)
        self.clients: dict[str, Client] = {}

        async with websockets.serve(self.handler, "localhost", 1200):
            Log.info("Server started on ws://localhost:1200")
            try:
                await self.game.run()
            except asyncio.CancelledError:
                Log.info("Server stopped.")

    async def handler(self, ws: ServerConnection) -> None:
        Log.info(f"New connection: {ws.remote_address}")
        client = Client(self, ws)
        try:
            async for message in ws:
                await client.process_message(str(message))
        except Exception as e:
            Log.error(f"Error in connection handler:\n{traceback.format_exc()}")
        finally:
            await client.unregister_all()
            self.remove(client)
            await ws.close()
            Log.info(f"Connection closed: {ws.remote_address}")

    def add(self, client: Client) -> None:
        if not client.uuid:
            Log.warn("Client UUID is not set.")
            return
        if client.uuid in self.clients:
            Log.warn(f"Client {client.uuid} already exists.")
            return
        self.clients[client.uuid] = client
        Log.info(f"Client {client.uuid} added.")

    def remove(self, client: Client) -> None:
        if not client.uuid:
            Log.warn("Client UUID is not set.")
            return
        if client.uuid not in self.clients:
            Log.warn(f"Client {client.uuid} not found.")
            return
        self.clients.pop(client.uuid)
        Log.info(f"Client {client.uuid} removed.")

    async def send_to(self, uuid: str, message: Message) -> None:
        await self.clients[uuid].queue_message(message)

    async def send_to_all_except(self, uuid: str, message: Message) -> None:
        for client in self.clients.values():
            if client.uuid != uuid:
                await client.queue_message(message)

    async def send_to_all(self, message: Message) -> None:
        for client in self.clients.values():
            await client.queue_message(message)

    async def update_clients(self) -> None:
        for client in self.clients.values():
            await client.send_all()
