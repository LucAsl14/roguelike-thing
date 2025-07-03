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
        self.border = WorldBorder(self)
        self.add(self.player)
        self.add(self.camera)
        self.add(self.border)
        self.constructs: list[Construct] = []
        self.projectiles: list[Projectile] = []
        self.enemies: list[Enemy] = []
        self.collideable_buckets = defaultdict(lambda: defaultdict(list))
        self.BUCKET_GRID_SIZE = 64

        for _ in range(30):
            self.add(Spawnpoint(self, Vec(uniform(-1000, 1000), uniform(-1000, 1000))))
        # self.add(TerrainBackground(self))

    def predraw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 160, 80))

        self.collideable_buckets = defaultdict(lambda: defaultdict(list))
        for construct in self.constructs:
            key = self.spacial_hash_key(construct.pos)
            self.collideable_buckets[key]["construct"].append(construct)
        for projectile in self.projectiles:
            key = self.spacial_hash_key(projectile.pos)
            self.collideable_buckets[key]["projectile"].append(projectile)
        for enemy in self.enemies:
            key = self.spacial_hash_key(enemy.pos)
            self.collideable_buckets[key]["entity"].append(enemy)
        self.collideable_buckets[self.spacial_hash_key(self.player.pos)]["entity"].append(self.player)

    def spacial_hash_key(self, pos: Vec) -> Vec:
        return Vec(pos.x // self.BUCKET_GRID_SIZE, pos.y // self.BUCKET_GRID_SIZE)
