from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from abc import abstractmethod
from .construct import Construct

class Projectile(Spell):
    def __init__(self, scene: MainScene, lifespan: float, speed: float, charge_time: float, dmg: int, elem: str, radius: int) -> None:
        super().__init__(scene, charge_time, elem)
        self.vel = Vec()
        self.pos = self.scene.player.pos.copy()
        self.speed = speed
        self.lifespan = LoopTimer(lifespan, 1)
        self.rect = pygame.Rect()
        self.damage = dmg
        self.rad = radius
        self.screen_pos = Vec()
        self.ignore_elem = []
        self.scene.projectiles.append(self)

    def kill(self) -> None:
        if not self.killed:
            self.scene.projectiles.remove(self)
        super().kill()

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
        self.rect = pygame.Rect(self.pos - (self.rad, self.rad), (self.rad * 2, self.rad * 2))
        if self.lifespan.done:
            self.kill()
            return
        # collision with constructs and projectiles
        for construct in self.scene.constructs:
            if self.rect.colliderect(construct.rect):
                self.collide(construct)
        for projectile in self.scene.projectiles:
            if self.rect.colliderect(projectile.rect) and \
               projectile.element not in self.ignore_elem and \
               projectile != self:
                self.collide(projectile)

    def set_screen_pos(self, screen: Surface) -> None:
        self.screen_pos = Vec(self.pos.x - self.scene.player.pos.x, self.scene.player.pos.y - self.pos.y)
        self.screen_pos += (screen.width / 2, screen.height / 2)

    def take_damage(self, dmg: int) -> int:
        """
        Returns:
            Amount of damage taken
        """
        prev_dmg = self.damage
        self.damage -= dmg
        if self.damage <= 0:
            self.damage = 0
            self.kill()
        return prev_dmg - self.damage

    @abstractmethod
    def collide(self, target: Construct | Projectile) -> None:
        dmg_dealt = target.take_damage(self.damage)
        self.take_damage(dmg_dealt)
