from boardwrapper import BoardWrapper
class MockClient():
    def __init__(self):
        self.falsestream = [
            {"type": "gameFull", "white": {"id": "whenchess", "name": "whenchess"}, "black": {"id": "opponent", "name": "opponent"}, "state": {"moves": "", "status": "started"}},
            {"type": "gameState", "moves": "e2e4 e7e5", "status": "started"},
            {"type": "gameState", "moves": "e2e4 d7d5 e4d5 d8d5 b1c3 e7e6", "status": "started"},
            {"type": "gameState", "moves": "e2e4 e7e5 d1f3 g8c6 f1c4 d7d6 f3f7", "status": "mate", "winner": "white"}
        ]
        self.moves = []
        #self.streamcounter = 0
        self.board = BoardWrapper()
    def stream(self):
        #yield self.falsestream[self.streamcounter]
        #self.streamcounter+=1
        yield self.falsestream[0]
        yield self.falsestream[1]
        yield self.falsestream[2]

    def makemockmove(self, move: str):
        self.moves.append(move)
        
        #self.falsestream.append({"type": "gameState", "moves": self.falsestream[len(self.falsestream) - 1]["moves"] + move, "status": self.status})
