from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from client.scenes.main_scene import MainScene

from shared.shared import Outgoing, serialize, Message
from client.core.debug import Log
from client.settings import URL
import websockets
import traceback
import asyncio

class Network:
    def __init__(self, scene: MainScene) -> None:
        self.scene = scene
        self.ws = None
        self.outgoing_sprites: dict[str, Outgoing] = {}
        self.queue: asyncio.Queue[Message] = asyncio.Queue()
        self.queue_lock = asyncio.Lock()

        self.send_event = asyncio.Event()
        self.send_event.clear()

        self.connected = False

    async def connect(self) -> None:
        while not self.connected:
            Log.info(f"Connecting to server at {URL}")
            try:
                async with websockets.connect(URL) as self.ws:
                    self.connected = True
                    Log.info("Connected to server.")
                    await asyncio.gather(self.send(), self.receive())
            except ConnectionRefusedError:
                Log.error("Failed to connect to server.")
                Log.info("Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def send(self) -> None:
        assert self.ws is not None, "WebSocket connection is not established."

        while self.connected:
            await self.send_event.wait()

            sprite_updates = []
            for sprite in self.outgoing_sprites.values():
                sprite_updates.append(dict(sprite.get_attributes()))
            message: Message = {
                "type": "update",
                "recipient": "all",
                "uuid": self.scene.player.uuid,
                "content": sprite_updates,
            }
            await self.ws.send(serialize(message))

            async with self.queue_lock:
                while not self.queue.empty():
                    message = await self.queue.get()
                    await self.ws.send(serialize(message))

            self.send_event.clear()

    async def receive(self) -> None:
        assert self.ws is not None, "WebSocket connection is not established."

        while self.connected:
            try:
                if message := await self.ws.recv():
                    self.scene.process_message(str(message))
            except websockets.ConnectionClosed:
                self.connected = False
                break
            except Exception as e:
                Log.error(f"Error receiving message:\n{traceback.format_exc()}")
                break

        await self.ws.close()
