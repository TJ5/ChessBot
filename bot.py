from boardwrapper import BoardWrapper
import chess
from movetree import MoveTreeNode
class Bot():
    def __init__(self, piececolor: str, fen = chess.STARTING_FEN):
        self.board = BoardWrapper(chess.Board(fen))
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
    def updateboardall(self, moves: str):
        self.board = self.board.updateboardall(moves)
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
            tree = MoveTreeNode(self.board, 0, 4, self.piececolor)
            move = tree.getbestmove()
            
            return move
        else:
            return None
        
    
    def getboard(self):
        return self.board.getboard()
    

    #gets a heuristic evaluation of the board
    def shalloweval(self):
        return self.board.shalloweval(self.piececolor)