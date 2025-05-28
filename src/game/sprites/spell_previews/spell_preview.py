from __future__ import annotations
from src.core import *

class SpellPreview(Sprite):
    def __init__(self, scene: MainScene, spell: Callable, cooldown: float, args: list) -> None:
        super().__init__(scene, "DEFAULT")
        self.scene = scene
        self.spell = spell
        self.cooldown = cooldown
        self.args = args.copy()

    def update(self, dt: float) -> None:
            if MOUSEBUTTONDOWN in self.game.events:
                self.trigger_spell()
                self.kill()

    def draw(self, target: pygame.Surface) -> None:
        pass

    def trigger_spell(self) -> None:
        self.scene.player.spell_queue.spend_top_spell()
        spell = self.spell(self.scene, self.game.mouse_pos - self.scene.player.screen_pos, "player", *self.args)
        self.scene.add(spell)
        spell.trigger_spell()
