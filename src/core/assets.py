from __future__ import annotations

from src.core.util import pathof, Storage
import pygame

def load_image(file: str, scale: int = 1) -> pygame.Surface:
    return pygame.transform.scale_by(pygame.image.load(pathof(f"res/images/{file}")).convert_alpha(), scale)

class Images(metaclass=Storage["Images", pygame.Surface]):
    def __init__(self) -> None:
        self.test = load_image("test.png")
        self.player = load_image("player.png")
    pygame.font.init()
    font = [pygame.font.Font(pathof("res/fonts/PixelTandysoft-0rJG.ttf"), i) for i in range(1, 129)]


# NOTE to future self: the following can be done:
# class SpriteSheets(metaclass=StorageSingletonMeta["SpriteSheets", SpriteSheet]):
#     def __init__(self) -> None:
#         self.player = SpriteSheet("player.png", 32, 32)
