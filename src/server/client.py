from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from server.server import Server

from shared.shared import SharedTemplate, backup_decoder, serialize, Message
from server.sprites import sprite_classes
from websockets import ServerConnection
from server.logger import Log
from typing import Any
import traceback
import asyncio
import json

class Client:
    def __init__(self, server: Server, ws: ServerConnection) -> None:
        self.server = server
        self.game = server.game
        self.ws = ws
        self.uuid = "UNKNOWN"
        self.registered: dict[str, SharedTemplate] = {}
        self.initialized = False

        self.queue: asyncio.Queue[Message] = asyncio.Queue()
        self.queue_lock = asyncio.Lock()

    def initialize(self, uuid: str) -> None:
        self.uuid = uuid
        self.server.add(self)
        self.initialized = True

    async def process_message(self, message: str) -> None:
        try:
            data = json.loads(message, object_hook=backup_decoder)
            # Log.info(f"Received message: {data}")

            if not self.initialized:
                self.initialize(data["uuid"])

            # Propagate the message to the appropriate recipient
            # "all" for all clients, "none" for no one, or a specific UUID
            match data["recipient"]:
                case "all":
                    await self.server.send_to_all_except(self.uuid, data)
                case recipient if recipient in self.server.clients:
                    await self.server.send_to(recipient, data)
                case "none": # Messages that other clients don't need to see
                    pass # Handle "none" case if needed
                case _:
                    Log.warn(f"Recipient {data["recipient"]} not found.")

            if data["type"] == "update":
                self.process_update(data)

        except json.JSONDecodeError as e:
            Log.error(f"JSON decode error:\n{traceback.format_exc()}")
        except Exception as e:
            Log.error(f"Error processing message:\n{traceback.format_exc()}")

    def process_update(self, data: Message) -> None:
        updates: list[dict[str, Any]] = data["content"]
        for update in updates:
            type: str = update["_type"]
            uuid: str = update["uuid"]

            # If the sprite is not in the game, add it
            if uuid not in self.game.sprites:
                if type not in sprite_classes:
                    Log.warn(f"Sprite type {type} not found.")
                    continue
                try:
                    update = update.copy()
                    update.pop("_type")
                    sprite = sprite_classes[type](**update)
                except TypeError:
                    Log.error(f"Argument mismatch for sprite type {type}: {update}")
                    continue
                self.register(sprite)
            # If the sprite is in the game, update it
            else:
                self.game.sprites[uuid].apply(update)

    async def queue_message(self, message: Message) -> None:
        async with self.queue_lock:
            await self.queue.put(message)

    async def send_all(self) -> None:
        async with self.queue_lock:
            while not self.queue.empty():
                message = await self.queue.get()
                await self.ws.send(serialize(message))

    def register(self, sprite: SharedTemplate) -> None:
        self.registered[sprite.uuid] = sprite
        self.game.add(sprite)

    async def unregister(self, sprite: SharedTemplate) -> None:
        self.registered.pop(sprite.uuid)
        self.game.remove(sprite)
        await self.server.send_to_all_except(self.uuid, {
            "type": "kill",
            "recipient": "none",
            "uuid": self.uuid,
            "content": {
                "uuid": sprite.uuid
            }
        })

    async def unregister_all(self) -> None:
        for sprite in list(self.registered.values()):
            await self.unregister(sprite)
