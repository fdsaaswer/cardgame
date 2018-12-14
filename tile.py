from card_type import CardType


class Tile():
    def __init__(self, land):
        self.unit = None
        self.enchantment = None
        self.land = land
        self.current_power = 0
        self.current_defense = 0

    def play_card(self, target, player, enemy, card):
        if card.land_type != self.land:
            return
        if card.type == CardType.CREATURE:
            self.unit = card
            self.current_power = card.base_power
            self.current_defense = card.base_defense
        elif card.type == CardType.ENCHANTMENT:
            self.enchantment = card
        elif card.type == CardType.SPELL:
            pass
        if card.on_create:
            card.on_create(target, player, enemy)

    def on_attack(self, target, player, enemy):
        pass

    def on_die(self, player, enemy):
        for idx, tile in enumerate(player.tiles):
            if self == tile:
                player.tiles[idx].unit = None
