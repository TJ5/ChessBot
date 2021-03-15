from boardwrapper import BoardWrapper
import chess
from value import SquareValue
class Bot():
    def __init__(self, piececolor: str):
        self.board = BoardWrapper()
        self.piececolor = piececolor
        if (self.piececolor == "white"):
            self.piececolor = chess.WHITE
        else:
            self.piececolor = chess.BLACK
    #updates board representing game state and returns move to make, if applicable
    def updateboard(self, moves: str):
        self.board = self.board.updateboard(moves)
        
        #return None if the latest update has created a draw by repetition and ended the game
        #return True if the game is still continuing
        if (self.board.isrepetition()):
            return None
        return True
        
    #resets board, then makes every move in the provided move string
    #for testing purposes, for inputting an arbitrary position
    def updateboardtest(self, moves: str):
        self.board = self.board.updateboardtest(moves)
        #check if it is the bot's turn to play, if so, return move
        if (self.board.isrepetition()):
            return None
        return True
    #Gets any legal move, without logic
    #To be changed
    def getmove(self):
        #return move if it is the bot's turn to play]
        #else, ignore
        if (self.board.getturn() == self.piececolor):
            moves : chess.LegalMoveGenerator = self.board.getmoves()
            moves = list(moves)
            
            i = 0
            currenteval = self.shalloweval()
            bestchange = -20000 #tracks best eval change from current state to candidate moves
            bestmove = None
            
            while (i < len(moves)):
                self.board.pushmove(moves[i])
                
                
                
                if ((self.shalloweval() - currenteval) > bestchange):
                    bestchange = self.shalloweval() - currenteval
                    bestmove = moves[i]
                self.board.popmove()
                i = i + 1

            return chess.Move.uci(bestmove)
        else:
            return None
        
    
    def getboard(self):
        return self.board.getboard()
    

    #gets a heuristic evaluation of the board
    def shalloweval(self):
        return self.board.shalloweval(self.piececolor)