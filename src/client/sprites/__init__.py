from .player import LocalPlayer, RemotePlayer
from .test_decoration import TestDecoration
from .inventory import Inventory
from .spell_queue import SpellQueue
from .spell import Spell
from .projectile import Projectile
from .fireball import Fireball
from .construct import Construct
from .earth_block import EarthBlock
from .waterball import Waterball
from .gust import Gust
from .stone_cannon import StoneCannon
from .area_spell import AreaSpell
from .steam import Steam
from .mud import Mud
from .whirlpool import Whirlpool
from .rollout import Rollout
from .camera import Camera
from .wall_of_fire import WallOfFire
from .world_border import WorldBorder

from client.core import Sprite
sprite_classes: dict[str, type[Sprite]] = {
    "Player": RemotePlayer,
}
