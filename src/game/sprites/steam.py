from __future__ import annotations

from pygame import Surface
from src.core import *
from .area_spell import AreaSpell

class Steam(AreaSpell):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 0, "air", 20, 125)
        self.circle_offsets: list[tuple[float, float]] = []
        self.new_circle = LoopTimer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        pass

    def draw_spell(self, screen: Surface) -> None:
        self.set_screen_pos(screen)
        for point in self.circle_offsets:
            screen_pos = self.screen_pos + point
            pygame.draw.circle(screen, (195, 195, 195), screen_pos, 50)

    def random_circle_point(self) -> tuple[float, float]:
        angle = uniform(0, 2*pi)
        scalar = uniform(0, self.rad)
        return (cos(angle) * scalar, sin(angle) * scalar)

    def update_spell(self, dt: float) -> None:
        if self.new_circle.done:
            self.circle_offsets.append(self.random_circle_point())
        super().update_spell(dt)

    def trigger_spell(self) -> None:
        for _ in range(10):
            self.circle_offsets.append(self.random_circle_point())
        super().trigger_spell()
