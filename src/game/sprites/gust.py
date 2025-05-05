from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .enemy import Enemy
class Gust(Spell):
    def __init__(self, scene: MainScene, target_posdiff: Vec, size: Vec, push: float, angle: float, hitbox: Hitbox) -> None:
        super().__init__(scene, 0, "air")
        self.angle = angle
        self.hitbox = hitbox
        self.size = size
        self.push = push
        self.pos = self.scene.player.pos
        self.anim_timer = Timer(0.3)

    def draw_charge(self, screen: Surface) -> None:
        pass
    def update_charge(self, dt: float) -> None:
        pass

    def update_spell(self, dt: float) -> None:
        if self.anim_timer.done:
            self.kill()

    def draw_spell(self, screen: Surface) -> None:
        player = self.scene.player
        screen_pos = player.screen_pos + 690 * self.anim_timer.progress * Vec(
                                   cos(self.angle), sin(self.angle)) + (
                                   uniform(-50, 50), uniform(-50, 50))
        pygame.draw.circle(screen, AIR, screen_pos, 10)

    def trigger_spell(self) -> None:
        for projectile in self.scene.projectiles:
            if projectile.element != "air" and projectile.pos.distance_to(self.pos) < projectile.rad + self.size.magnitude() \
            and self.hitbox.is_colliding(projectile.hitbox):
                change = (400 * 10 / projectile.rad) * Vec(1, 0).rotate(degrees(self.angle))
                projectile.external_acc += change
        for enemy in self.scene.enemies:
            if enemy.pos.distance_to(self.pos) < self.size.magnitude() + enemy.size.magnitude() \
            and self.hitbox.is_colliding(enemy.hitbox):
                change = (400 * 70 / enemy.size.magnitude()) * Vec(1, 0).rotate(degrees(self.angle))
                enemy.ext_acc += change
        self.scene.player.ext_acc = (-40 * self.push) * Vec(1, 0).rotate(degrees(self.angle))
        self.anim_timer.reset()
