from __future__ import annotations
from src.core import *

from .inventory import Inventory
from .test_decoration import TestDecoration
from .spell_queue import SpellQueue
from src.core.util.hitbox import Hitbox # I actually don't get why this is necessary

class Player(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "DEFAULT")
        # band-aid fix to scene not considered MainScene
        self.scene = scene

        # movement-related variables
        self.pos = Vec()
        self.vel = Vec()
        self.acc = Vec()
        self.ext_acc = Vec()
        self.CONST_ACCEL = 3300

        # inventory
        self.inventory = Inventory(self.scene)
        for _ in range(10):
            self.inventory.add("water")
            self.inventory.add("fire")
            self.inventory.add("earth")
            self.inventory.add("air")
        self.scene.add(self.inventory)

        # spell queue
        self.spell_queue = SpellQueue(self.scene)
        self.scene.add(self.spell_queue)

        # player visuals and hitbox
        self.image = Image.get("player")
        rect = self.image.get_rect()
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(rect.width, rect.height)
        self.angle = 0

    def update(self, dt: float) -> None:
        self.update_keys(dt)
        self.update_position(dt)
        self.update_surroundings()

    def draw(self, target: pygame.Surface) -> None:
        self.image = pygame.transform.rotate(Image.get("player"), self.angle)
        target.blit(self.image, self.screen_pos - Vec(self.image.get_rect().size) / 2)


    def update_keys(self, dt: float) -> None:
        self.keys = pygame.key.get_pressed()

        # movement keys
        if self.keys[K_w] and self.keys[K_s]:
            self.acc.y = -sign(self.vel.y) * self.CONST_ACCEL
        elif self.keys[K_w]:
            self.acc.y = -self.CONST_ACCEL
        elif self.keys[K_s]:
            self.acc.y = self.CONST_ACCEL
        else:
            self.acc.y = 0

        if self.keys[K_a] and self.keys[K_d]:
            self.acc.x = -sign(self.vel.x) * self.CONST_ACCEL
        elif self.keys[K_d]:
            self.acc.x = self.CONST_ACCEL
        elif self.keys[K_a]:
            self.acc.x = -self.CONST_ACCEL
        else:
            self.acc.x = 0

        # spell keys
        if KEYDOWN in self.game.events:
            match self.game.key_down:
                case pygame.K_j | pygame.K_1:
                    if self.inventory.take("water"):
                        self.spell_queue.push("water")
                case pygame.K_i | pygame.K_2:
                    if self.inventory.take("air"):
                        self.spell_queue.push("air")
                case pygame.K_k | pygame.K_3:
                    if self.inventory.take("earth"):
                        self.spell_queue.push("earth")
                case pygame.K_l | pygame.K_4:
                    if self.inventory.take("fire"):
                        self.spell_queue.push("fire")
                case pygame.K_SPACE:
                    if len(self.spell_queue.queue) and self.spell_queue.queue[-1] != " ":
                        self.spell_queue.push(" ")
                case pygame.K_BACKSPACE:
                    removed = self.spell_queue.remove()
                    if removed != "" and removed != " ":
                        self.inventory.add(removed)

        # press a button to make decorations lol (NOT a feature)
        if self.keys[K_q]:
            self.scene.add(TestDecoration(self.scene, self.pos + (uniform(-100, 100), uniform(-100, 100))))
        # debug key
        if self.keys[K_p]:
            Log.debug(self.scene.projectiles)

    def update_position(self, dt: float) -> None:
        self.vel += self.acc * dt
        self.vel += self.ext_acc
        self.ext_acc = Vec()
        self.vel *= 0.004 ** dt
        self.pos += self.vel * dt
        self.hitbox.set_position(self.pos)
        self.hitbox.set_rotation(self.angle)

    def update_surroundings(self) -> None:
        # something something about generating decorations im too lazy
        pass
