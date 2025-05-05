from __future__ import annotations
from src.core import *
from .projectile import Projectile
from pygame import Surface

from typing import TYPE_CHECKING
class Waterball(Projectile):
    def __init__(self, scene: MainScene, target_posdiff: Vec) -> None:
        super().__init__(scene, target_posdiff, 5, 400, 1.5, 10, "water", 20)
        self.exploding = False
        self.exploding_timer = Timer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        pygame.draw.circle(screen, WATER, self.screen_pos, self.rad * self.charging_time.progress)

    def update_spell(self, dt: float) -> None:
        super().update_spell(dt)
        if self.exploding:
            self.rad = 20 + 180 * self.exploding_timer.progress
            if self.exploding_timer.done:
                # testing an exploding mechanic
                self.hitbox.set_size_rad(200)
                for construct in self.scene.constructs:
                    if self.pos.distance_to(construct.pos) < self.rad + construct.size.magnitude() and \
                       self.hitbox.is_colliding(construct.hitbox):
                        construct.take_damage(10)
                for projectile in self.scene.projectiles:
                    if self.pos.distance_to(projectile.pos) < self.rad + projectile.rad and \
                       projectile.element != self.element and self.hitbox.is_colliding(projectile.hitbox):
                        projectile.take_damage(10)
                for enemy in self.scene.enemies:
                    if self.pos.distance_to(enemy.pos) < self.rad + enemy.size.magnitude() and \
                       self.hitbox.is_colliding(enemy.hitbox):
                        enemy.take_damage(10)
                # self-damage. Remove this?
                # if self.pos.distance_to(self.scene.player.pos) < self.rad + self.scene.player.size.magnitude() and \
                #    self.hitbox.is_colliding(self.scene.player.hitbox):
                #     self.scene.player.take_damage(10)
                super().kill()


    def draw_spell(self, screen: Surface) -> None:
        pygame.draw.circle(screen, WATER, self.screen_pos, self.rad)

    def kill(self) -> None:
        if not self.exploding:
            self.exploding_timer.reset()
        self.exploding = True
        self.vel = Vec()
