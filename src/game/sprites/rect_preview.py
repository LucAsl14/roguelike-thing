from __future__ import annotations
from src.core import *
from .spell_preview import SpellPreview
class RectPreview(SpellPreview):
    def __init__(self, scene: MainScene, spell: Callable, cooldown: float, args: list) -> None:
        super().__init__(scene, spell, cooldown, args)
        self.rect: Vec = args[0]

    def draw(self, target: pygame.Surface) -> None:
        mpos = self.game.mouse_pos
        player = self.scene.player
        self.angle = 90 - degrees(atan2((mpos.y - player.screen_pos.y), (mpos.x - player.screen_pos.x)))
        origimg = pygame.surface.Surface(self.rect)
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, (120, 120, 120), origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, self.angle)
        target.blit(rotimg, mpos - Vec(rotimg.size) / 2)

    def trigger_spell(self) -> None:
        self.args.append(self.angle)
        super().trigger_spell()
