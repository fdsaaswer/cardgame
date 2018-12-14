from land_type import LandType
from player import Player
from tile import Tile

SAMPLE_DECK = [0, 1, 2, 3, 4, 5, 6]


class GameServer:

    def __init__(self):
        self.players = [Player(20, SAMPLE_DECK[:5], SAMPLE_DECK[6:], [Tile(LandType.PLAIN)] * 4),
                        Player(20, SAMPLE_DECK[:5], SAMPLE_DECK[6:], [Tile(LandType.PLAIN)] * 4)]
        self.active = 0

    def next_turn(self):
        next = 1 - self.active
        self.players[self.active].end_turn(self.players[next])
        self.active = next
