from __future__ import annotations
from src.core import *

from .area_spell import AreaSpell
from pygame import Surface

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
class WallOfFire(AreaSpell):
    def __init__(self, scene: MainScene, target_posdiff: Vec, rad: int) -> None:
        super().__init__(scene, target_posdiff, 9999, "fire", 15, rad, "GROUND")
        self.is_original = True
        self.wall_segments = 20
        self.prev_pos = Vec()
        self.damage_timer = LoopTimer(0.05)
        self.original_wall = self

    def draw_charge(self, screen: Surface) -> None:
        if self.is_original:
            trans_surf = pygame.surface.Surface(Vec(self.rad * 2), pygame.SRCALPHA)
            pygame.draw.circle(trans_surf, FIRE + (100,), Vec(self.rad), self.rad)
            self.pos = self.game.mouse_pos + self.scene.camera.pos
            screen.blit(trans_surf, self.screen_pos - Vec(self.rad))
        else:
            trans_surf = pygame.surface.Surface(Vec(2 * self.rad), pygame.SRCALPHA)
            pygame.draw.circle(trans_surf, FIRE, Vec(self.rad), self.rad)
            trans_surf.set_alpha(184)
            screen.blit(trans_surf, self.screen_pos - Vec(self.rad))

    def update_charge(self, dt: float) -> None:
        if self.original_wall.wall_segments <= 1:
            self.trigger_spell()
            self.charging_time.force_end()
        if self.is_original:
            self.pos = self.game.mouse_pos + self.scene.camera.pos

            # on first wall
            if self.wall_segments == 20:
                spell = WallOfFire(self.scene, Vec(), self.rad)
                self.scene.add(spell)
                spell.pos = self.pos.copy()
                spell.is_original = False
                spell.original_wall = self
                self.wall_segments -= 1
                self.prev_pos = self.pos
                return

            diff = self.pos - self.prev_pos

            # on subsequent walls
            while diff.magnitude() > self.rad:
                self.prev_pos += diff.normalize() * self.rad
                diff = self.pos - self.prev_pos
                temp_pos = self.pos - diff
                spell = WallOfFire(self.scene, Vec(), self.rad)
                self.scene.add(spell)
                spell.pos = temp_pos
                spell.is_original = False
                spell.original_wall = self
                self.wall_segments -= 1

    def draw_spell(self, screen: Surface) -> None:
        pygame.draw.circle(screen, tuple(map(sum, zip(FIRE, (10, -40, -40)))), self.screen_pos, self.rad)
        # fire particles?

    # TODO: should probably also make player take damage
    def update_spell(self, dt: float) -> None:
        # reduces damage of all projectiles coming into contact
        # should it buff "fire" type projectiles?
        if self.damage_timer.done:
            for proj in self.scene.projectiles:
                if proj.pos.distance_to(self.pos) <= proj.rad + self.rad:
                    proj.take_damage(1)
        super().update_spell(dt)
