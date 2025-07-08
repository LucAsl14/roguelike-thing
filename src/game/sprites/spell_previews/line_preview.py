from __future__ import annotations
from src.core import *
from .spell_preview import SpellPreview

class LinePreview(SpellPreview):
    def __init__(self, scene: MainScene, spell: Callable, cooldown: float, args: list) -> None:
        super().__init__(scene, spell, cooldown, args)

    def draw(self, target: pygame.Surface) -> None:
        pygame.draw.line(target, (120, 120, 120), self.scene.player.screen_pos, self.game.mouse_pos, 3)
