from __future__ import annotations

from pygame import Surface
from src.core import *
from .construct import Construct
class TestDecoration(Construct):
    def __init__(self, scene: MainScene, pos: Vec) -> None:
        super().__init__(scene, -1, -1, 10 + choice(range(0, 6)))
        self.pos = pos
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rad(20)
        self.size = Vec(20)

    def draw_spell(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, tuple(map(sum, zip((150, 50, 50), (-6*self.hp, 2*self.hp, 2*self.hp)))), self.screen_pos, 20)

    def draw_charge(self, screen: Surface) -> None:
        pass
