from __future__ import annotations
from src.core import *

class City(Sprite):
    def __init__(self, scene: MainScene, pos: Vec) -> None:
        super().__init__(scene, "GROUND")
        self.image = Image.get("city").copy()
        self.pos = pos

    def update(self, dt: float) -> None:
        pass

    def draw(self, target: pygame.Surface) -> None:
        target.blit(self.image, self.screen_pos)
