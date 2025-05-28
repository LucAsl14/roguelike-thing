from __future__ import annotations
from src.core import *
from .spell_preview import SpellPreview

class GustPreview(SpellPreview):
    def __init__(self, scene: MainScene, spell: Callable, cooldown: float, args: list) -> None:
        super().__init__(scene, spell, cooldown, args)
        self.size = args[0]
        self.push = args[1]
        self.hitbox = Hitbox(Vec(100000), []) # send this so far away... to avoid that ONE frame of ugliness
        self.hitbox.set_size_rect(self.size.x, self.size.y)
        self.hitbox.translate(Vec(0, self.size.y / 2))

    def update(self, dt: float) -> None:
        self.pos = self.scene.player.pos
        self.hitbox.set_rotation(self.angle - pi/2, False)
        self.hitbox.set_position(self.pos)
        super().update(dt)

    def draw(self, target: pygame.Surface) -> None:
        mpos = self.game.mouse_pos
        player = self.scene.player
        self.angle = atan2((mpos.y - player.screen_pos.y), (mpos.x - player.screen_pos.x)) # in radians
        flipped_angle = self.angle + pi
        pygame.draw.line(target, (120, 120, 120), player.screen_pos, player.screen_pos + Vec(0, self.push).rotate(-90 + degrees(flipped_angle)), 5)
        rotangle = -degrees(self.angle) + 90
        origimg = pygame.surface.Surface(self.size, pygame.SRCALPHA)
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, (120, 120, 120, 100), origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, rotangle)
        target.blit(rotimg, player.screen_pos + self.size.y / 2 * Vec(1, 0).rotate(degrees(self.angle)) - Vec(rotimg.size) / 2)
        # hitbox debugging
        if Debug.on():
            pygame.draw.polygon(target, (255, 0, 0), [Vec(p) - self.scene.player.pos + self.scene.player.screen_pos for p in self.hitbox.get_hitbox()], 2)

    def trigger_spell(self) -> None:
        self.args.append(self.angle)
        self.args.append(self.hitbox)
        super().trigger_spell()
