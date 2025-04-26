from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import LocalPlayer

from pygame import Surface
from .construct import Construct
from client.core import *
from .projectile import Projectile

class Fireball(Projectile):
    def __init__(self, scene: MainScene, owner: Optional[LocalPlayer]) -> None:
        super().__init__(scene, owner, 10, 800, 0.5, 10, "fire", 10)

    def draw_charge(self, screen: Surface) -> None:
        pygame.draw.circle(screen, FIRE, self.screen_pos, self.rad * self.charging_time.progress)

    def draw_spell(self, screen: Surface) -> None:
        pygame.draw.circle(screen, FIRE, self.screen_pos, self.rad)

    def collide(self, target: Construct | Projectile | LocalPlayer) -> None:
        super().collide(target)
        self.kill()
