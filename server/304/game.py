"""
game
"""

class Game:
    """
    304 game
    """

    def __init__(self, sid:str) -> None:
        self.sid = sid
        self.players = []
        self.state = "waiting"
