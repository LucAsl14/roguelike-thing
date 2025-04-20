from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from .construct import Construct

class Projectile(Spell):
    def __init__(self, scene: MainScene, lifespan: float, speed: float, charge_time: float, dmg: int, elem: str, radius: int) -> None:
        super().__init__(scene, charge_time, elem)
        self.vel = Vec()
        self.external_acc = Vec()
        self.pos = self.scene.player.pos.copy()
        self.speed = speed
        self.lifespan = Timer(lifespan)
        self.rect = pygame.Rect()
        self.damage = dmg
        self.rad = radius
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
        self.lifespan.reset()
        super().trigger_spell()

    def update_spell(self, dt: float) -> None:
        self.vel += self.external_acc
        self.pos += self.vel * dt
        self.external_acc = Vec()

        self.rect = pygame.Rect(self.pos - Vec(self.rad), Vec(self.rad * 2))
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

    def collide(self, target: Construct | Projectile) -> None:
        dmg_dealt = target.take_damage(self.damage)
        self.take_damage(dmg_dealt)
        if dmg_dealt > 0:
            Log.debug(f"{self} dealt {dmg_dealt} dmg to {target}")
