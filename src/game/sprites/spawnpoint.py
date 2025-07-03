from __future__ import annotations
from src.core import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player

class Spawnpoint(Sprite): # maybe also act as tp points?
    def __init__(self, scene: MainScene, pos: Vec) -> None:
        super().__init__(scene, "GROUND")
        self.scene = scene

        self.collected = False
        self.selected = False

        self.pos = pos

        # visuals
        self.image = Image.get("spawnpoint").copy()
        rect = self.image.get_rect()
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(rect.width, rect.height)
        self.size = Vec(rect.width, rect.height)

        self.col_tint = pygame.Surface(self.image.get_size()).convert_alpha()
        self.col_tint.fill((0, 0, 150, 150))
        self.sel_tint = pygame.Surface(self.image.get_size()).convert_alpha()
        self.sel_tint.fill((0, 200, 0, 100))

    def draw(self, target: pygame.Surface):
        img = self.image.copy()
        if self.collected:
            img.blit(self.col_tint, (0, 0))
        if self.selected:
            img.blit(self.sel_tint, (0, 0))
        target.blit(img, self.screen_pos - Vec(self.image.get_rect().size) / 2)

    def update(self, dt: float):
        if self.colliding_player():
            self.collected = True
            if not self.selected:
                self.selected = True
                self.scene.player.update_spawnpoint(self)
                # Log.debug(f"Spawnpoint at {self.pos} collected by player at {self.scene.player.pos}")


    def colliding_player(self) -> bool:
        self_rad = (self.size.x + self.size.y) / 2
        player = self.scene.player
        player_rad = (player.size.x + player.size.y) / 2
        is_close = player.pos.distance_squared_to(self.pos) < (self_rad + player_rad) ** 2

        if is_close and self.hitbox.is_colliding(player.hitbox):
            return True
        return False
