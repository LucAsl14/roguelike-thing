from __future__ import annotations

from pygame import Surface
from src.core import *
from src.game.sprites.common import Entity
from src.game.sprites import *
from collections import defaultdict

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
        self.entity_buckets = defaultdict(list[Entity])
        self.player = Player(self)
        self.camera = Camera(self, self.player)
        self.add(self.player)
        self.add(self.camera)
        # self.constructs: list[Construct] = []
        # self.projectiles: list[Projectile] = []
        # self.enemies: list[Enemy] = []

        # self.add(TerrainBackground(self))

    def predraw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 160, 80))

    def postdraw(self, screen: Surface) -> None:
        if Debug.on():
            for bucket in self.entity_buckets.values():
                for entity in bucket:
                    entity.hitbox.draw(screen, self.camera.pos)

    def spacial_hash_key(self, pos: Vec) -> Vec:
        return Vec(pos.x // BUCKET_GRID_SIZE, pos.y // BUCKET_GRID_SIZE)

    @property
    def world_mouse_pos(self) -> Vec:
        return self.game.mouse_pos + self.camera.pos
