from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from server.server import Server

from server.logger import Log
from server.settings import *
from server.sprites import *
from shared.shared import *
import asyncio

class Game:
    def __init__(self, server: Server) -> None:
        self.server = server
        self.sprites: dict[str, SharedTemplate] = {}

    def add(self, sprite: SharedTemplate) -> None:
        if sprite.uuid in self.sprites:
            Log.warn(f"Sprite with UUID {sprite.uuid} already exists.")
            return
        self.sprites[sprite.uuid] = sprite

    def remove(self, sprite: SharedTemplate) -> None:
        if sprite.uuid not in self.sprites:
            Log.warn(f"Sprite with UUID {sprite.uuid} does not exist.")
            return
        self.sprites.pop(sprite.uuid)

    async def run(self) -> None:
        while True:
            start_time = asyncio.get_event_loop().time()

            self.update()
            await self.queue_messages()
            await self.server.update_clients()

            elapsed = asyncio.get_event_loop().time() - start_time
            await asyncio.sleep(max(0, 1 / TPS - elapsed))

    def update(self) -> None:
        # Run any sprite logic here
        pass

    async def queue_messages(self) -> None:
        # Any data that the server calculated that should be sent to the
        # clients should be queued here. This does not include messages that
        # are in response to a client's message (like propagating it).
        pass
