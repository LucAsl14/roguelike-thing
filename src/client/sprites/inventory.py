from __future__ import annotations
from client.core import *

class Inventory(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "HUD")
        self.elements = {
            "air": 0,
            "water": 0,
            "earth": 0,
            "fire": 0
        }

    def update(self, dt: float) -> None:
        pass

    def draw(self, target: pygame.Surface) -> None:
        self.pos = Vec(300, target.get_height() - 100)
        # kinda redundant but it is what it is
        if self.elements["water"] > 0:
            pygame.draw.rect(target, WATER, pygame.Rect(self.pos.x, self.pos.y, 50, 50))
            target.blit(Font.get("font18").render(str(self.elements["water"]), False, (0, 0, 0)), (self.pos + (50, 45)))
            target.blit(Font.get("font18").render("J", False, (16, 16, 0)), (self.pos + (50 - 40, 15)))
        if self.elements["air"] > 0:
            pygame.draw.rect(target, AIR, pygame.Rect(self.pos.x + 60, self.pos.y, 50, 50))
            target.blit(Font.get("font18").render(str(self.elements["air"]), False, (0, 0, 0)), (self.pos + (110, 45)))
            target.blit(Font.get("font18").render("I", False, (16, 16, 0)), (self.pos + (110 - 40, 15)))
        if self.elements["earth"] > 0:
            pygame.draw.rect(target, EARTH, pygame.Rect(self.pos.x + 120, self.pos.y, 50, 50))
            target.blit(Font.get("font18").render(str(self.elements["earth"]), False, (0, 0, 0)), (self.pos + (170, 45)))
            target.blit(Font.get("font18").render("K", False, (16, 16, 0)), (self.pos + (170 - 40, 15)))
        if self.elements["fire"] > 0:
            pygame.draw.rect(target, FIRE, pygame.Rect(self.pos.x + 180, self.pos.y, 50, 50))
            target.blit(Font.get("font18").render(str(self.elements["fire"]), False, (0, 0, 0)), (self.pos + (230, 45)))
            target.blit(Font.get("font18").render("L", False, (16, 16, 0)), (self.pos + (230 - 40, 15)))

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
