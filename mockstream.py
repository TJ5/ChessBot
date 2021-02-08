class MockStream():
    def __init__(self):
        self.falsestream = [
            {"type": "gameFull", "white": {"id": "whenchess", "name": "whenchess"}, "black": {"id": "opponent", "name": "opponent"}},
            {"type": "gameState", "moves": "e2e4 e7e5", "status": "started"},
            {"type": "gameState", "moves": "e2e4 e7e5 d1f3 g8c6 f1c4 d7d6 f3f7", "status": "mate", "winner": "white"}
        ]
    def stream(self):
        yield self.falsestream[0]
        yield self.falsestream[1]
        yield self.falsestream[2]