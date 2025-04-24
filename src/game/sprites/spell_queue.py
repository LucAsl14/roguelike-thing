from __future__ import annotations
from src.core import *
from .fireball import Fireball
from .earth_block import EarthBlock
from .waterball import Waterball
from .gust import Gust
from .stone_cannon import StoneCannon
from .steam import Steam
from .mud import Mud
from .whirlpool import Whirlpool
from .rollout import Rollout
from .wall_of_fire import WallOfFire

class SpellQueue(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "HUD")
        self.queue = []
        self.scene = scene
        self.cursor_timer = LoopTimer(0.5, -1)
        self.cursor_blink_on = True
        self.aiming_spell = None
        self.spell_list = {
            "j": Waterball,
            "k": EarthBlock,
            "i": Gust,
            "l": Fireball,
            "kl": StoneCannon, "lk": StoneCannon, # temporarily doubling up until Andrew teaches me
            "jl": Steam, "lj": Steam,
            "kj": Mud, "jk": Mud,
            "ij": Whirlpool, "ji": Whirlpool,
            "ik": Rollout, "ki": Rollout,
            "il": WallOfFire, "li": WallOfFire,
        }

    def update(self, dt: float) -> None:
        if self.cursor_timer.done:
            self.cursor_blink_on = not self.cursor_blink_on
        self.parse_top_spell()

    def draw(self, target: pygame.Surface) -> None:
        self.pos = Vec(200, target.get_height() - 180)
        trans_surf = pygame.surface.Surface((target.get_width() - 400, 70), pygame.SRCALPHA)
        pygame.draw.rect(trans_surf, (120, 120, 120, 100), pygame.Rect((0, 0), (target.get_width() - 400, 70)))
        for i in range(len(self.queue)):
            draw_pos = Vec(10 + 60 * i, 10)
            if self.queue[i] == " " or draw_pos.x > target.get_width() - 400:
                continue
            color = (0, 0, 0)
            match self.queue[i]:
                case "water":
                    color = WATER + (200,)
                case "air":
                    color = AIR + (200,)
                case "earth":
                    color = EARTH + (200,)
                case "fire":
                    color = FIRE + (200,)
            pygame.draw.rect(trans_surf, color, pygame.Rect(draw_pos, (50, 50)))
        draw_pos = Vec(10 + 60 * len(self.queue), 10)
        target.blit(trans_surf, self.pos)
        if draw_pos.x <= 400 and self.cursor_blink_on:
            pygame.draw.rect(trans_surf, (0, 0, 0, 200), pygame.Rect(draw_pos, (5, 50)))
        target.blit(trans_surf, self.pos)


    def push(self, item: str) -> None:
        """
        Adds an element to the back of the queue.
        """
        self.queue.append(item)
        if self.aiming_spell:
            self.aiming_spell.kill()
            self.aiming_spell = None

    def remove(self) -> str:
        """
        Removes the element at the back of the queue.

        Returns:
            The element that was removed, an empty string if it failed.
        """
        if len(self.queue) == 0:
            return ""
        if self.aiming_spell:
            self.aiming_spell.kill()
            self.aiming_spell = None
        return self.queue.pop()

    def pop(self) -> str:
        """
        Removes the element at the front of the queue.

        Returns:
            The element that was removed, an empty string if it failed.
        """
        if len(self.queue) == 0:
            return ""
        return self.queue.pop(0)

    def get_top_string(self) -> str:
        """
        Get a simplified version of the topmost string of sigils.

        Returns:
            topmost string of sigils, e.g. "iji" for ["air", "water", "air"]
        """
        string = ""
        for i in range(len(self.queue)):
            if self.queue[i] == " ":
                break
            match self.queue[i]:
                case "water":
                    string += "j"
                case "air":
                    string += "i"
                case "earth":
                    string += "k"
                case "fire":
                    string += "l"
        return string

    def parse_top_spell(self) -> None:
        spell = self.spell_list.get(self.get_top_string())
        if spell != None and not self.aiming_spell:
            self.aiming_spell = spell(self.scene)
            self.scene.add(self.aiming_spell)

    def spend_top_spell(self) -> None:
        while len(self.queue) and self.queue[0] != " ":
            top_elem = self.pop()
            if self.aiming_spell != None:
                self.scene.player.inventory.add(top_elem, self.aiming_spell.cooldown)
        if len(self.queue):
            self.pop()
        self.aiming_spell = None
