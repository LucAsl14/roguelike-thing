from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

class AreaSpell(Spell):
    def __init__(self, scene: MainScene, charge_time: float, elem: str, lifespan: float, radius: int) -> None:
        super().__init__(scene, charge_time, elem)
        self.lifespan = Timer(lifespan)
        self.rad = radius
        self.pos = Vec()
        self.screen_pos = Vec()

    def update_charge(self, dt: float) -> None:
        pass

    def update_aiming(self, dt: float) -> None:
        posdiff = (self.game.mouse_pos - self.scene.player.screen_pos)
        posdiff.y *= -1
        self.pos = self.scene.player.pos + posdiff

    def draw_aiming(self, screen: Surface) -> None:
        trans_surf = pygame.surface.Surface((self.rad * 2, self.rad * 2), pygame.SRCALPHA)
        pygame.draw.circle(trans_surf, (120, 120, 120, 100), (self.rad, self.rad), self.rad)
        self.screen_pos = self.game.mouse_pos
        screen.blit(trans_surf, self.screen_pos - (self.rad, self.rad))

    def update_spell(self, dt: float) -> None:
        if self.lifespan.done:
            self.kill()

    def trigger_spell(self) -> None:
        self.lifespan.reset()
        super().trigger_spell()

    def set_screen_pos(self, screen: Surface) -> None:
        self.screen_pos = Vec(self.pos.x - self.scene.player.pos.x, self.scene.player.pos.y - self.pos.y)
        self.screen_pos += (screen.width / 2, screen.height / 2)
