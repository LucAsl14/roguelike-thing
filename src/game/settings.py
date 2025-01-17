from enum import Enum, auto
from src.core.util.general import pathof
import pygame


class Layer(Enum):
    BACKGROUND = auto()
    GROUND = auto()
    DEFAULT = auto()
    SKY = auto()
    HUD = auto()

TITLE = "Game"
WIDTH = 960
HEIGHT = 540
SIZE = WIDTH, HEIGHT

# I'm tired of copying color values over soo
FIRE = (200, 100, 50)
EARTH = (100, 60, 30)
AIR = (200, 200, 200)
WATER = (50, 100, 200)
