from __future__ import annotations

from pygame import Surface
from .construct import Construct
from src.core import *
from .projectile import Projectile

class Fireball(Projectile):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 10, 800, 0.5, 10, "fire", 10)

    def draw_charge(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        self.set_screen_pos(screen)
        pygame.draw.circle(screen, (200, 100, 50), self.screen_pos, self.charging_time.elapsed * self.rad / self.charging_time.duration)

    def draw_spell(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        self.set_screen_pos(screen)
        pygame.draw.circle(screen, (200, 100, 50), self.screen_pos, self.rad)

    def collide(self, target: Construct | Projectile) -> None:
        super().collide(target)
        self.kill()
