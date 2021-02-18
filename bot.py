from boardwrapper import BoardWrapper
import chess
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
            move = self.board.getmove()
            ucimove = chess.Move.uci(move)
            return ucimove
        else:
            return None
        
    
    def getboard(self):
        return self.board.getboard()
    