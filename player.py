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

    def to_html(self, is_active):
        text = '<p>{} ({}/{})</p>'.format(self.name, self.actions, self.health)
        for idx, tile in enumerate(self.tiles):
            text += tile.to_html(is_active, idx)
        for idx, card in enumerate(self.hand):
            text += """<form action="" method="post">
                       <table><tr>{}</tr><tr><td>
                       <input type="submit" value="{}" name="Play card" {}/>
                       </td><td>
                       <input type="text" name="target_id"></td></tr></table>
                       </form>""".format(card.to_html(), idx, None if is_active else "disabled")
        text += """<form action="" method="post">
                   <input type="submit" value="Draw card" name="Draw card" {}/>
                   </form>""".format(None if is_active else "disabled")
        text += """<form action="" method="post">
                   <input type="submit" value="End turn" name="End turn" {}/>
                   </form>""".format(None if is_active else "disabled")
        return text

    def use_card(self, enemy):
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

    def draw_card(self):
        if not self.actions:
            raise GameLogicError("No more actions remaining")
        if len(self.deck) == 0:
            raise GameLogicError("Deck is empty")
        card = self.deck.pop()
        self.hand.append(card)
        self.actions -= 1

    def end_turn(self, enemy):
        for idx, tile in enumerate(self.tiles):
            # tile.end_turn(enemy.tiles[idx], self, enemy) # needs lane id
            if not tile.unit:
                return
            if tile.actions == 0:
                return
            # self.on_attack(target, self, enemy)
            if enemy.tiles[idx].unit:
                enemy.tiles[idx].current_defense -= tile.current_power
                tile.current_defense -= enemy.tiles[idx].current_power
                if enemy.tiles[idx].current_defense <= 0:
                    # target.on_die(enemy, self)
                    enemy.tiles[idx] = None
            else:
                enemy.health -= tile.current_power
            tile.actions = 1
        self.actions = 2
