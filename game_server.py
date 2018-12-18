from random import shuffle

from card import Card
from exception import GameLogicError
from land_type import LandType
from player import Player
from tile import Tile

SAMPLE_DECK_1 = [Card(x) for x in [0, 1, 2, 3, 4, 5, 6]]
SAMPLE_DECK_2 = [Card(x) for x in [0, 1, 2, 3, 4, 5, 6]]


class GameServer:

    def __init__(self):
        shuffle(SAMPLE_DECK_1)
        shuffle(SAMPLE_DECK_2)
        self.players = [Player("Player 1", 20, SAMPLE_DECK_1[:5], SAMPLE_DECK_1[6:], [Tile(LandType.PLAIN)] * 4),
                        Player("Player 2", 20, SAMPLE_DECK_2[:5], SAMPLE_DECK_2[6:], [Tile(LandType.CORNFIELD)] * 4)]
        self.active = 0

    def draw_card(self):
        raise GameLogicError("Not implemented")

    def use_card(self):
        raise GameLogicError("Not implemented")

    def play_card(self, pos_id, target_id):
        player = self.players[self.active]
        enemy = self.players[1 - self.active]
        player.play_card(enemy, pos_id, target_id)

    def next_turn(self):
        next = 1 - self.active
        self.players[self.active].end_turn(self.players[next])
        self.active = next