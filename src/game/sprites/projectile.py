from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from .construct import Construct

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
class Projectile(Spell):
    def __init__(self, scene: MainScene, owner: Optional[Player], lifespan: float, speed: float, charge_time: float, dmg: int, elem: str, radius: int) -> None:
        super().__init__(scene, owner, charge_time, elem)
        self.vel = Vec()
        self.external_acc = Vec()
        self.pos = self.scene.player.pos.copy()
        self.speed = speed
        self.lifespan = Timer(lifespan)
        self.rad = radius
        self.damage = dmg
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rad(radius)
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

        self.hitbox.set_position(self.pos)

        if self.lifespan.done:
            self.kill()
            return
        # collision with anything collidable
        for construct in self.scene.constructs:
            if self.pos.distance_to(construct.pos) < self.rad + construct.size.magnitude() and \
               self.hitbox.is_colliding(construct.hitbox):
                self.collide(construct)
        for projectile in self.scene.projectiles:
            if self.pos.distance_to(projectile.pos) < self.rad + projectile.rad and \
               projectile.element not in self.ignore_elem and \
               projectile != self and self.hitbox.is_colliding(projectile.hitbox):
                self.collide(projectile)
        if self.owner != self.scene.player and \
           self.pos.distance_to(self.scene.player.pos) < self.rad + self.scene.player.size.magnitude() and \
           self.hitbox.is_colliding(self.scene.player.hitbox):
            self.collide(self.scene.player)

    def take_damage(self, dmg: int) -> int:
        """
        Returns:
            Amount of damage taken
        """
        if self.aiming:
            return 0
        prev_dmg = self.damage
        self.damage -= dmg
        if self.damage <= 0:
            self.damage = 0
            self.kill()
        return prev_dmg - self.damage

    def collide(self, target: Construct | Projectile | Player) -> None:
        dmg_dealt = target.take_damage(self.damage)
        self.take_damage(dmg_dealt)
        if dmg_dealt > 0:
            Log.debug(f"{self} dealt {dmg_dealt} dmg to {target}")
