from card import CardType
from exception import GameLogicError


class Player:

    def __init__(self, name, health, hand, deck, tiles):
        self.name = name
        self.health = health
        self.hand = hand
        self.deck = deck
        self.tiles = tiles
        self.actions = 2

    def end_turn(self, enemy):
        for idx, tile in enumerate(self.tiles):
            if not tile.unit:
                continue
            target = enemy.tiles[idx]
            tile.on_attack(target, self, enemy)
            if target.unit:
                target.current_defense -= tile.current_power
                if target.current_defense <= 0:
                    target.on_die(enemy, self)
            else:
                enemy.health -= tile.current_power

    def draw_card(self):
        pass

    def play_card(self, enemy, pos_id, target_id):
        try:
            card = self.hand.pop(pos_id)
        except KeyError as e:
            raise GameLogicError("No such card in hand")

        try:
            if card.type == CardType.CREATURE:
                if target_id is None:
                    raise GameLogicError("Not implemented yet - should iterate all fields")
                if self.tiles[target_id].unit:
                    raise GameLogicError("Position {} already taken".format(target_id))
                self.tiles[target_id].unit = card

            if card.type == CardType.ENCHANTMENT:
                if target_id is None:
                    raise GameLogicError("Not implemented yet - should iterate all fields")
                if self.tiles[target_id].enchantment:
                    raise GameLogicError("Position {} already taken".format(target_id))
                self.tiles[target_id].enchantment = card

            if card.type == CardType.SPELL:
                raise GameLogicError("Not implemented")
        except GameLogicError as e:
            self.hand.append(card)
            raise e

    def use_card(self):
        pass