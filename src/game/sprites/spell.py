from __future__ import annotations
from src.core import *
from abc import abstractmethod
from pygame.locals import MOUSEBUTTONDOWN

class Spell(Sprite):
    def __init__(self, scene: MainScene, charge_time: float, elem: str, layer: str = "DEFAULT") -> None:
        super().__init__(scene, layer)
        self.aiming = True
        self.scene = scene
        self.charging_time = Timer(charge_time)
        self.element = elem
        self.killed = False

    def update(self, dt: float) -> None:
        if self.killed:
            return
        if self.aiming:
            self.update_aiming(dt)
            if MOUSEBUTTONDOWN in self.game.events:
                self.trigger_spell()
                self.aiming = False
        elif not self.charging_time.done:
            self.update_charge(dt)
        else:
            self.update_spell(dt)

    def draw(self, target: pygame.Surface) -> None:
        if self.aiming:
            self.draw_aiming(target)
        elif not self.charging_time.done:
            self.draw_charge(target)
        else:
            self.draw_spell(target)

    def kill(self) -> None:
        if not self.killed:
            super().kill()
        self.killed = True

    @abstractmethod
    def draw_aiming(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def draw_spell(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def draw_charge(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def update_aiming(self, dt: float) -> None:
        pass

    @abstractmethod
    def update_spell(self, dt: float) -> None:
        pass

    @abstractmethod
    def update_charge(self, dt: float) -> None:
        pass

    @abstractmethod
    def trigger_spell(self) -> None:
        if self.aiming:
            self.scene.player.spell_queue.spend_top_spell()
        self.charging_time.reset()
