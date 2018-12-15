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

    def play_card(self, enemy, card_id, pos_id, target_id):
        card = self.hand(card_id)

    def use_card(self):
        pass