from __future__ import annotations

from pygame import Surface
from .construct import Construct
from src.core import *
from .projectile import Projectile

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .enemy import Enemy
    from .player import Player
class Fireball(Projectile):
    def __init__(self, scene: MainScene, target_posdiff: Vec, origin: str) -> None:
        super().__init__(scene, target_posdiff, 10, 800, 0.5, 10, "fire", 10, origin)

    def draw_charge(self, screen: Surface) -> None:
        pygame.draw.circle(screen, FIRE, self.screen_pos, self.rad * self.charging_time.progress)

    def draw_spell(self, screen: Surface) -> None:
        pygame.draw.circle(screen, FIRE, self.screen_pos, self.rad)

    def collide(self, target: Construct | Projectile | Enemy | Player) -> None:
        super().collide(target)
        self.kill()
