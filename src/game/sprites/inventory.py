from __future__ import annotations
from src.core import *
from typing import List

class Inventory(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "HUD")
        self.elements = {
            "air": 0,
            "water": 0,
            "earth": 0,
            "fire": 0
        }
        self.cooling = {
            "air": 0,
            "water": 0,
            "earth": 0,
            "fire": 0
        }
        self.spent_elements: List[tuple[Timer, str, int]] = []

        # trying to simplify the draw() redundancy
        self.to_draw = [
            ("water", WATER, "J"),
            ("air",   AIR,   "I"),
            ("earth", EARTH, "K"),
            ("fire",  FIRE,  "L")
        ]

    def update(self, dt: float) -> None:
        for (timer, elem, num) in self.spent_elements:
            if timer.done:
                self.spent_elements.remove((timer, elem, num))
                self.add(elem, num = num)
                self.cooling[elem] -= num

    def draw(self, target: pygame.Surface) -> None:
        self.pos = Vec(300, target.get_height() - 100)
        # kinda redundant but it is what it is
        for i, (elem, color, tag) in enumerate(self.to_draw):
            if self.cooling[elem] > 0:
                # damn you pylance for causing these next 2 lines
                darker = [c/2 for c in color]
                new_darker: tuple[int, int, int] = (int(darker[0]), int(darker[1]), int(darker[2]))
                pygame.draw.rect(target, new_darker, pygame.Rect(self.pos + Vec(60 * i, 0), Vec(50)))
                target.blit(Font.get("font18").render(str(self.cooling[elem]), False, (80, 80, 80)), (self.pos + (60 * i + 5, 45)))
            if self.elements[elem] > 0:
                pygame.draw.rect(target, color, pygame.Rect(self.pos + Vec(60 * i, 0), Vec(50)))
                target.blit(Font.get("font18").render(str(self.elements[elem]), False, (0, 0, 0)), (self.pos + (60 * i + 35, 45)))
                target.blit(Font.get("font18").render(tag, False, (16, 16, 0)), (self.pos + (60 * i + 10, 15)))



    def add(self, elem: str, cooldown: float = 0, num = 1) -> None:
        """Add an element to the inventory."""
        if cooldown == 0:
            self.elements[elem] += num
        else:
            self.spent_elements.append((Timer(cooldown), elem, num))
            self.cooling[elem] += num

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
