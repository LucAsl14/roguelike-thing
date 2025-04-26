from __future__ import annotations
from client.sprites import *
from shared.shared import *
from client.core import *
import asyncio
import json

class MainScene(Scene):
    _layers = [
        LayerGroup.record().add(
            Layer.record("BACKGROUND"),
            Layer.record("GROUND"),
            Layer.record("DEFAULT"),
            Layer.record("SKY"),
            Layer.record("HUD"),
        )
    ]

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.network = Network(self)
        asyncio.create_task(self.network.connect())
        self.send_timer = PreciseLoopTimer(1 / TPS)

        self.player = LocalPlayer(self)
        self.camera = Camera(self, self.player)
        self.border = WorldBorder(self)
        self.add(self.player)
        self.add(self.camera)
        self.add(self.border)
        self.constructs: list[Construct] = []
        self.projectiles: list[Projectile] = []

        for _ in range(1000):
            self.add(TestDecoration(self, Vec(uniform(-self.border.rad, self.border.rad), uniform(-self.border.rad, self.border.rad))))

    def postupdate(self, dt: float) -> None:
        if self.send_timer.done:
            self.network.send_event.set()

    def predraw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 160, 80))

    def process_message(self, message: str) -> None:
        """Receives the full raw message as a string from the server."""
        # Log.debug(f"Received message: {message}")
        data: Message = json.loads(message, object_hook=backup_decoder)

        if data["type"] == "update":
            self.process_update(data)
        elif data["type"] == "kill":
            self.process_kill(data)

    def process_update(self, data: Message) -> None:
        updates: list[dict[str, Any]] = data["content"]
        for update in updates:
            type: str = update["_type"]
            uuid: str = update["uuid"]
            # If the sprite is not in the game, add it
            if uuid not in self.sprite_mapping:
                if type not in sprite_classes:
                    Log.warn(f"Sprite type {type} not found.")
                    continue
                update = update.copy()
                update.pop("_type")
                sprite = sprite_classes[type](self, **update)
                self.add(sprite)
            # If the sprite is in the game, update it
            else:
                sprite = self.sprite_mapping[uuid]
                if not isinstance(sprite, SharedTemplate):
                    Log.warn(f"Sprite {uuid} of type {type} is not a SharedTemplate, "
                             "hence cannot be updated by remote.")
                    continue
                sprite.apply(update)

    def process_kill(self, data: Message) -> None:
        content: dict[str, Any] = data["content"]
        uuid: str = content["uuid"]
        if uuid in self.sprite_mapping:
            self.remove(self.sprite_mapping[uuid])
        else:
            Log.warn(f"Server sent kill message for sprite {uuid} that is not in the game.")

    def add(self, sprite: Sprite) -> None:
        super().add(sprite)
        if isinstance(sprite, Outgoing):
            self.network.outgoing_sprites[sprite.uuid] = sprite

    def remove(self, sprite: Sprite) -> None:
        super().remove(sprite)
        if isinstance(sprite, Outgoing):
            self.network.outgoing_sprites.pop(sprite.uuid)
