from __future__ import annotations
from src.core import *
from src.game.sprites import *

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.player = Player(self)
        self.add(self.player)

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((120, 160, 80))
        self.sprite_manager.draw(screen)
