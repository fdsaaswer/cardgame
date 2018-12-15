from card_type import CardType
from land_type import LandType


class Card:
    def __init__(self, id):
        # Use DB-lookup for this
        if id == 0:
            self.name = "Soldier"
            self.description = "Base creature for testing"
            self.type = CardType.CREATURE
            self.base_power = 2
            self.base_defense = 10
            self.land_type = LandType.PLAIN
        elif id == 1:
            self.name = "Tower"
            self.description = "Base building for testing"
            self.type = CardType.ENCHANTMENT
            self.land_type = LandType.PLAIN | LandType.CORNFIELD
        else:
            self.name = "Wall"
            self.description = "Protective wall"
            self.type = CardType.CREATURE
            self.base_power = 0
            self.base_defense = 20
