from __future__ import annotations
from src.core import *

class Inventory(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, Layer.HUD)
        self.screen_pos = Vec()
        self.elements = {
            "air": 0,
            "water": 0,
            "earth": 0,
            "fire": 0
        }

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        self.screen_pos = Vec(300, screen.get_height() - 100)
        # kinda redundant but it is what it is
        if self.elements["water"] > 0:
            pygame.draw.rect(screen, (50, 100, 200), pygame.Rect(self.screen_pos.x, self.screen_pos.y, 50, 50))
            screen.blit(Images.font[18].render(str(self.elements["water"]), False, (0, 0, 0)), (self.screen_pos + (50, 45)))
            screen.blit(Images.font[18].render("J", False, (16, 16, 0)), (self.screen_pos + (50 - 40, 15)))
        if self.elements["air"] > 0:
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(self.screen_pos.x + 60, self.screen_pos.y, 50, 50))
            screen.blit(Images.font[18].render(str(self.elements["air"]), False, (0, 0, 0)), (self.screen_pos + (110, 45)))
            screen.blit(Images.font[18].render("I", False, (16, 16, 0)), (self.screen_pos + (110 - 40, 15)))
        if self.elements["earth"] > 0:
            pygame.draw.rect(screen, (100, 60, 30), pygame.Rect(self.screen_pos.x + 120, self.screen_pos.y, 50, 50))
            screen.blit(Images.font[18].render(str(self.elements["earth"]), False, (0, 0, 0)), (self.screen_pos + (170, 45)))
            screen.blit(Images.font[18].render("K", False, (16, 16, 0)), (self.screen_pos + (170 - 40, 15)))
        if self.elements["fire"] > 0:
            pygame.draw.rect(screen, (200, 100, 50), pygame.Rect(self.screen_pos.x + 180, self.screen_pos.y, 50, 50))
            screen.blit(Images.font[18].render(str(self.elements["fire"]), False, (0, 0, 0)), (self.screen_pos + (230, 45)))
            screen.blit(Images.font[18].render("L", False, (16, 16, 0)), (self.screen_pos + (230 - 40, 15)))

    def add(self, elem: str, num = 1) -> None:
        """Add an element to the inventory."""
        self.elements[elem] += num

    def take(self, elem: str, num = 1) -> bool:
        """
        Remove an element from the inventory.
        Will fail when trying to remove more than what is currently being held.

        Returns:
            whether an element was successfully removed
        """
        if (self.elements[elem] < num):
            return False
        self.elements[elem] -= num
        return True
