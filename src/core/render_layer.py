from src.core.sprite import Sprite
from enum import Enum, auto
import pygame

class RenderLayer:
    def __init__(self) -> None:
        self.updating_sprites: list[Sprite] = []
        self.rendering_sprites: list[Sprite] = []
        self.bound_sprites: dict[Sprite, Sprite] = {}

    def update(self, dt: float) -> None:
        for sprite in self.updating_sprites:
            sprite.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.rendering_sprites:
            self._draw_sprite(sprite, screen)

    def _draw_sprite(self, sprite: Sprite, screen: pygame.Surface) -> None:
        sprite.draw(screen)
        # Recursively draw bound sprites
        if sprite in self.bound_sprites:
            self._draw_sprite(self.bound_sprites[sprite], screen)
            self._draw_sprite(self.bound_sprites[sprite], screen)

    def add(self, sprite: Sprite) -> None:
        self.updating_sprites.append(sprite)
        if isinstance(sprite, Sprite):
            self.rendering_sprites.append(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.updating_sprites.remove(sprite)
        if isinstance(sprite, Sprite):
            self.rendering_sprites.remove(sprite)

    def bind(self, bottom: Sprite, top: Sprite) -> None:
        if top in self.bound_sprites:
            # Generate a trace of the cyclical binding
            stack = [current := top]
            while current in self.bound_sprites:
                stack.append(current := self.bound_sprites[current])
            trace = " -> ".join(map(str, stack))
            raise ValueError(f"Cyclical binding detected: \n{trace}")

        try:
            self.remove(top)
        except ValueError:
            # top either doesn't exist in the layer or has been removed
            # from being having been bound to another sprite
            pass
        self.bound_sprites[bottom] = top

    def unbind(self, bottom: Sprite) -> bool:
        if bottom in self.bound_sprites:
            del self.bound_sprites[bottom]
            return True
        return False

    def __len__(self) -> int:
        return len(self.updating_sprites) + len(self.bound_sprites)
