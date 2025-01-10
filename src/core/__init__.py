from src.game.settings import *

from .sprite import Sprite
from .assets import Images
from .scene import Scene
from .util import *
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.scenes import *
    from .game import Game
