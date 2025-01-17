from __future__ import annotations
from src.core import *

class TestDecoration(Sprite):
    def __init__(self, scene: MainScene, pos: Vec) -> None:
        super().__init__(scene, Layer.GROUND)
        self.pos = pos
        # once again, band-aid fix for scene not being properly cast
        self.scene = scene

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        screen_pos = self.pos - self.scene.player.pos + self.scene.player.screen_pos
        pygame.draw.circle(screen, (10, 10, 10), screen_pos, 20)
