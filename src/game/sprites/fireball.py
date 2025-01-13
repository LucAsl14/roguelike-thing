from __future__ import annotations

from pygame import Surface
from .construct import Construct
from src.core import *
from .projectile import Projectile

class Fireball(Projectile):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 10, 800, 0.5, 10, "fire")

    def draw_charge(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        screen_pos = Vec(self.pos.x - self.scene.player.pos.x, self.scene.player.pos.y - self.pos.y)
        screen_pos += (screen.width / 2, screen.height / 2)
        pygame.draw.circle(screen, (200, 100, 50), screen_pos, self.charging_time.elapsed * 10 / 0.5)

    def draw_spell(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        screen_pos = Vec(self.pos.x - self.scene.player.pos.x, self.scene.player.pos.y - self.pos.y)
        screen_pos += (screen.width / 2, screen.height / 2)
        pygame.draw.circle(screen, (200, 100, 50), screen_pos, 10)
        self.rect = pygame.Rect(self.pos - (5, 5), (10, 10))

    def collide(self, target: Construct | Projectile) -> None:
        super().collide(target)
        Log.info(f"me: {self} colliding with {target}")
        self.kill()
