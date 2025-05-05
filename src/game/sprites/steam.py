from __future__ import annotations

from pygame import Surface
from src.core import *
from .area_spell import AreaSpell

# TODO: probably change this spell because it's useless in pve
class Steam(AreaSpell):
    def __init__(self, scene: MainScene, target_posdiff: Vec, rad: int) -> None:
        super().__init__(scene, target_posdiff, 0, "water", 20, rad, "SKY")
        self.circle_offsets: list[Vec] = []
        self.new_circle = LoopTimer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        pass

    def draw_spell(self, screen: Surface) -> None:
        for point in self.circle_offsets:
            screen_pos = self.screen_pos + point
            pygame.draw.circle(screen, (195, 195, 255), screen_pos, self.rad * 2 / 5)

    def random_circle_point(self) -> Vec:
        angle = uniform(0, 2*pi)
        scalar = uniform(0, self.rad)
        return scalar * Vec(cos(angle), sin(angle))

    def update_spell(self, dt: float) -> None:
        if self.new_circle.done:
            self.circle_offsets.append(self.random_circle_point())
        super().update_spell(dt)

    def trigger_spell(self) -> None:
        for _ in range(10):
            self.circle_offsets.append(self.random_circle_point())
        super().trigger_spell()
