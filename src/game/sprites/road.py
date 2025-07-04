from __future__ import annotations
from src.core import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .city import City

class Road(Sprite):
    def __init__(self, scene: MainScene, city1: City, city2: City) -> None:
        super().__init__(scene, "BACKGROUND")
        self.city1 = city1
        self.city2 = city2

    def update(self, dt: float) -> None:
        pass

    def draw(self, target: pygame.Surface) -> None:
        #TODO: make this into a bezier curve or something
        pygame.draw.line(
            target,
            (100, 80, 70),  # Color of the road
            self.city1.screen_pos,
            self.city2.screen_pos,
            width=100  # Width of the road
        )
