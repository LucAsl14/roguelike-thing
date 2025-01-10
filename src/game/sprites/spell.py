from __future__ import annotations
from src.core import *
from abc import abstractmethod
from pygame.locals import MOUSEBUTTONDOWN

class Spell(Sprite):
    def __init__(self, scene: MainScene, charge_time: float) -> None:
        super().__init__(scene, Layer.DEFAULT)
        self.aiming = True
        self.scene = scene
        self.charging_time = Timer(charge_time)

    def update(self, dt: float) -> None:
        if self.aiming:
            self.update_aiming(dt)
            if MOUSEBUTTONDOWN in self.game.events:
                self.aiming = False
                self.trigger_spell()
        elif not self.charging_time.done:
            self.update_charge(dt)
        else:
            self.update_spell(dt)

    def draw(self, screen: pygame.Surface) -> None:
        if self.aiming:
            self.draw_aiming(screen)
        elif not self.charging_time.done:
            self.draw_charge(screen)
        else:
            self.draw_spell(screen)

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
        self.scene.player.spell_queue.spend_top_spell()
        self.charging_time.reset()
