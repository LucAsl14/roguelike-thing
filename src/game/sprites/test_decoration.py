from __future__ import annotations

from pygame import Surface
from src.core import *
from .construct import Construct
class TestDecoration(Construct):
    def __init__(self, scene: MainScene, pos: Vec) -> None:
        super().__init__(scene, None, -1, -1, 10)
        self.pos = pos
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rad(20)
        self.size = Vec(20)

    def update_aiming(self, dt: float) -> None:
        self.aiming = False

    def draw_spell(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, (10, 10, 10), self.screen_pos, 20)

    def draw_aiming(self, screen: pygame.Surface) -> None:
        pass

    def draw_charge(self, screen: Surface) -> None:
        pass
