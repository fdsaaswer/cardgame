import Player

class GameServer:
    players = []

    def __init__(self):
        self.players.extend(Player())
