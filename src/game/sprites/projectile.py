from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from abc import abstractmethod
from .construct import Construct

class Projectile(Spell):
    def __init__(self, scene: MainScene, lifespan: float, speed: float, charge_time: float) -> None:
        super().__init__(scene, charge_time)
        self.vel = Vec()
        self.pos = self.scene.player.pos.copy()
        self.speed = speed
        self.lifespan = LoopTimer(lifespan, 1)
        self.rect = pygame.Rect()

    def update_charge(self, dt: float) -> None:
        pass

    def update_aiming(self, dt: float) -> None:
        self.pos = self.scene.player.pos.copy()

    def draw_aiming(self, screen: Surface) -> None:
        pygame.draw.line(screen, (120, 120, 120), self.scene.player.screen_pos, self.game.mouse_pos, 3)

    def trigger_spell(self) -> None:
        self.vel = (self.game.mouse_pos - self.scene.player.screen_pos).normalize() * self.speed
        self.vel.y *= -1
        self.lifespan.reset()
        super().trigger_spell()

    def update_spell(self, dt: float) -> None:
        self.pos += self.vel * dt
        if self.lifespan.done:
            self.kill()
            return
        # collision with own construct
        for construct in self.scene.player.constructs:
            if self.rect.colliderect(construct.rect):
                self.collide(construct)

    @abstractmethod
    def collide(self, target: Construct) -> None:
        pass
