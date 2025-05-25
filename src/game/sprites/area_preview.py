from __future__ import annotations
from src.core import *
from .spell_preview import SpellPreview

class AreaPreview(SpellPreview):
    def __init__(self, scene: MainScene, spell: Callable, cooldown: float, args: list) -> None:
        super().__init__(scene, spell, cooldown, args)
        self.rad = args[0] # fetching radius (probably the wrong way)

    def draw(self, target: pygame.Surface) -> None:
        trans_surf = pygame.surface.Surface(Vec(self.rad * 2), pygame.SRCALPHA)
        pygame.draw.circle(trans_surf, (120, 120, 120, 100), Vec(self.rad), self.rad)
        self.pos = self.game.mouse_pos + self.scene.camera.pos
        target.blit(trans_surf, self.screen_pos - (self.rad, self.rad))
