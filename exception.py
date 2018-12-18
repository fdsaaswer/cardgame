class GameLogicError(ValueError):
    def __init__(self, msg):
        ValueError.__init__(self, msg)
