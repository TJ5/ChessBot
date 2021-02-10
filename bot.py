from boardwrapper import BoardWrapper
import chess
class Bot():
    def __init__(self, pieces: str):
        self.board = BoardWrapper()
        self.pieces = pieces
        if (self.pieces == "white"):
            self.pieces = chess.WHITE
        else:
            self.pieces = chess.BLACK
    def updateboard(self, moves: str):
        self.board = self.board.updateboard(moves)
        print(self.board.getfen())
        if (self.board.getturn() == self.pieces):
            #print(self.board.getturn())
            return self.getmove()
            
        else:
            #print(self.board.getturn())
            pass
    def getmove(self):
        
        move = self.board.getmove()
           
        
        
        ucimove = chess.Move.uci(move)
        print(ucimove)
        return ucimove
        