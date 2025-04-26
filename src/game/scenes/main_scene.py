from __future__ import annotations
from src.core import *
from src.game.sprites import *

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

        for _ in range(1000):
            self.add(TestDecoration(self, Vec(uniform(-self.border.rad, self.border.rad), uniform(-self.border.rad, self.border.rad))))

    def predraw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 160, 80))
