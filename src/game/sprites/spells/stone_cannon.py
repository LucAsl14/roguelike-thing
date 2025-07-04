from __future__ import annotations

from pygame import Surface
from .construct import Construct
from src.core import *
from .projectile import Projectile

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..enemy import Enemy
class StoneCannon(Projectile):
    def __init__(self, scene: MainScene, target_posdiff: Vec, origin: str) -> None:
        super().__init__(scene, target_posdiff, 10, 700, 0, 5, "earth", 8, origin)
        self.iframe = Timer(0.75)
        self.angle = 0
        self.turn_speed = 2
        self.target_pos = Vec()
        self.target_posdiff = target_posdiff
        self.is_original = True

    def draw_charge(self, screen: Surface) -> None:
        pass
    def update_charge(self, dt: float) -> None:
        pass

    def draw_spell(self, screen: Surface) -> None:
        pygame.draw.circle(screen, EARTH, self.screen_pos, self.rad)
        pygame.draw.circle(screen, EARTH, self.screen_pos + 8 * Vec(cos(self.angle), sin(self.angle)), self.rad / 2)

    def update_spell(self, dt: float) -> None:
        self.vel = self.speed * Vec(cos(self.angle), sin(self.angle))
        # custom external acc handling
        self.vel += self.external_acc
        if self.external_acc.magnitude() > 0:
            self.angle = atan2(self.vel.y, self.vel.x)
            self.speed = self.vel.magnitude()
        self.external_acc = Vec()
        posdiff = self.target_pos - self.pos
        target_angle = atan2(posdiff.y, posdiff.x)
        degdiff = ((((self.angle - target_angle) * 180 / pi) % 360) + 360) % 360
        if degdiff <= 2 or degdiff >= 358:
            self.turn_speed = 0
            self.speed = 1000 # 1000
        elif degdiff < 180:
            self.angle -= self.turn_speed * dt
        else:
            self.angle += self.turn_speed * dt
        if self.turn_speed != 0 and self.speed > 0:
            self.speed = max(0, self.speed / 20 ** dt - 100 * dt)
            if self.speed < 1: self.speed = 0
        if self.speed == 0:
            self.turn_speed = 10
        super().update_spell(dt)

    def trigger_spell(self) -> None:
        if self.is_original:
            for _ in range(4):
                spell = StoneCannon(self.scene, self.target_posdiff, self.origin)
                self.scene.add(spell)
                spell.is_original = False
                spell.trigger_spell()
                spell.speed += int(uniform(-200, 201))
        player = self.scene.player
        screen_pos_diff = self.game.mouse_pos - player.screen_pos
        self.target_pos = screen_pos_diff + player.pos
        posdiff = self.target_pos - self.pos
        target_angle = atan2(posdiff.y, posdiff.x)
        self.angle = uniform(target_angle + pi - pi/4, target_angle + pi + pi/4)

    # def collide(self, target: Construct | Projectile | Enemy) -> None:
    #     # redundant for now
    #     if isinstance(target, StoneCannon):
    #         return
    #     super().collide(target)
