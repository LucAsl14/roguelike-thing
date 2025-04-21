from __future__ import annotations

from pygame import Surface
from core import *
from .area_spell import AreaSpell

class Steam(AreaSpell):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 0, "water", 20, 250, "SKY")
        self.circle_offsets: list[Vec] = []
        self.new_circle = LoopTimer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        pass

    def draw_spell(self, screen: Surface) -> None:
        for point in self.circle_offsets:
            screen_pos = self.screen_pos + point
            pygame.draw.circle(screen, (195, 195, 255), screen_pos, 100)

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
