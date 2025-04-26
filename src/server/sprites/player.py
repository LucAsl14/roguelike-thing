from shared import *
from util import *

class Player(T_Player, Outgoing):
    def __init__(self, uuid: str, pos: Vec):
        self.uuid = uuid
        self.pos = pos
        # print(self.__dict__)
