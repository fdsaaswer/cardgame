from card import CardType

class Tile():
    def __init__(self, land):
        self.unit = None
        self.enchantment = None
        self.land = land
        self.current_power = 0
        self.current_defense = 0
        self.actions = 1

    def to_html(self, is_active, idx):
        text = '<form action="" method="post"><table border = "1">'
        text += '<td>Land type: {}</td>'.format(self.land)
        if self.unit:
            text += '<td>{} {}/{}</td>'.format(self.unit.to_html(), self.current_power, self.current_defense)
            try:
                if self.unit.use:
                    text += '<input type="submit" value="{}" name="Use card" {}/>'. \
                        format(idx, None if is_active else "disabled")
            except AttributeError as e:
                pass
        else:
            text += '<td>No creature</td>'
        if self.enchantment:
            text += '<td>{}</td>'.format(self.enchantment.to_html())
            try:
                if self.enchantment.use:
                    text += '<input type="submit" value="{}" name="Use card" {}/>'. \
                        format(idx, None if is_active else "disabled")
            except AttributeError as e:
                pass
        else:
            text += '<td>No building</td>'
        text += '</table>'
        return text

    def use_card(self):
        pass

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

    def end_turn(self, target, player, enemy):
        pass

    def on_attack(self, target, player, enemy):
        pass

    def on_die(self, player, enemy):
        for idx, tile in enumerate(player.tiles):
            if self == tile:
                player.tiles[idx].unit = None
