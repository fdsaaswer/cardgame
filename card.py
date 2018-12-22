from enum import Enum
from enum import IntFlag


class LandType(IntFlag):
    PLAIN = 1
    CORNFIELD = 2

class CardType(Enum):
    CREATURE = 1
    ENCHANTMENT = 2
    SPELL = 3

class Card:
    def __init__(self, id):
        # Use DB-lookup for this
        if id == 0:
            self.name = "Soldier"
            self.description = "Base creature for testing"
            self.type = CardType.CREATURE
            self.land_type = LandType.PLAIN
            self.base_power = 2
            self.base_defense = 10
            self.action_cost = 1
        elif id == 1:
            self.name = "Tower"
            self.description = "Base building for testing"
            self.type = CardType.ENCHANTMENT
            self.action_cost = 1
        else:
            self.name = "Wall"
            self.description = "Protective wall"
            self.type = CardType.CREATURE
            self.land_type = LandType.PLAIN | LandType.CORNFIELD
            self.base_power = 0
            self.base_defense = 20
            self.action_cost = 1

    def to_html(self):
        # return str(self.__dict__)
        return self.name
