from __future__ import annotations
from core import *
from .projectile import Projectile
from pygame import Surface

class Waterball(Projectile):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 5, 400, 1.5, 10, "water", 20)
        self.exploding = False
        self.exploding_timer = Timer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        pygame.draw.circle(screen, WATER, self.screen_pos, self.rad * self.charging_time.progress)

    def update_spell(self, dt: float) -> None:
        super().update_spell(dt)
        if self.exploding:
            self.rad = 20 + 180 * self.exploding_timer.progress
            if self.exploding_timer.done:
                # testing an exploding mechanic
                self.rect = pygame.Rect(self.pos - (200, 200), (400, 400))
                for construct in self.scene.constructs:
                    if self.rect.colliderect(construct.rect):
                        construct.take_damage(10)
                for projectile in self.scene.projectiles:
                    if self.rect.colliderect(projectile.rect) and projectile.element != self.element:
                        projectile.take_damage(10)
                super().kill()


    def draw_spell(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        pygame.draw.circle(screen, WATER, self.screen_pos, self.rad)

    def kill(self) -> None:
        if self.aiming:
            super().kill()
        if not self.exploding:
            self.exploding_timer.reset()
        self.exploding = True
        self.vel = Vec()
