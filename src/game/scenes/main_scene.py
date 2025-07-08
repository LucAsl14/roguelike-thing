from __future__ import annotations
from src.core import *
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
        self.player = Player(self)
        self.camera = Camera(self, self.player)
        self.add(self.player)
        self.add(self.camera)
        # self.constructs: list[Construct] = []
        # self.projectiles: list[Projectile] = []
        # self.enemies: list[Enemy] = []
        self.entity_buckets = defaultdict(list)

        # self.add(TerrainBackground(self))

    def preupdate(self, dt: float) -> None:
        self.entity_buckets = defaultdict(list)

    def predraw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 160, 80))

    def spacial_hash_key(self, pos: Vec) -> Vec:
        return Vec(pos.x // BUCKET_GRID_SIZE, pos.y // BUCKET_GRID_SIZE)

    @property
    def world_mouse_pos(self) -> Vec:
        return self.game.mouse_pos + self.camera.pos
