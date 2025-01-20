from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

class Construct(Spell):
    def __init__(self, scene: MainScene, charge_time: float, lifespan: float, hp: int) -> None:
        """
        Notes: \n
        A lifespan of -1 grants the construct infinite duration \n
        An hp amount of -1 makes it indestructible
        """
        super().__init__(scene, charge_time, "earth")
        self.lifespan = Timer(lifespan)
        self.hp = hp
        self.pos: Vec
        self.scene.constructs.append(self)
        # pretty sure this is *not* how hitboxes are made
        self.rect = pygame.Rect()

    def update_charge(self, dt: float) -> None:
        pass
    def update_aiming(self, dt: float) -> None:
        pass

    def update_spell(self, dt: float) -> None:
        if self.rect.colliderect(self.scene.player.rect):
            self.collide_player()
        if self.lifespan.done:
            self.kill()
            return
        if self.hp == 0:
            self.kill()

    def trigger_spell(self) -> None:
        self.lifespan.reset()
        if self.aiming:
            screen_pos = self.game.mouse_pos - self.scene.player.screen_pos
            self.pos = self.scene.player.pos + screen_pos
            super().trigger_spell()

    def collide_player(self) -> None:
        self.scene.player.vel = Vec((self.scene.player.pos - self.pos))

    def take_damage(self, dmg: int) -> int:
        """
        Returns:
            actual damage taken
        """
        prev_hp = self.hp
        if self.hp == -1: return dmg
        self.hp = max(self.hp - dmg, 0)
        return prev_hp - self.hp

    def kill(self) -> None:
        if not self.killed:
            self.scene.constructs.remove(self)
        super().kill()
