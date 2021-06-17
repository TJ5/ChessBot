from boardwrapper import BoardWrapper
import chess
from movetree import MoveTreeNode
from endgame import EndgamePredictor
class Bot():
    def __init__(self, piececolor: str, fen = chess.STARTING_FEN):
        self.e = EndgamePredictor()
        self.board = BoardWrapper(self.e, chess.Board(fen))
        self.piececolor = piececolor
        if (self.piececolor == "white"):
            self.piececolor = chess.WHITE
            
        else:
            self.piececolor = chess.BLACK
        self.tree = None
        if (self.board.getturn() == self.piececolor):
            self.tree = MoveTreeNode(self.board, 0, 4, self.piececolor, self.e)
    #updates board representing game state and returns move to make, if applicable
    def updateboard(self, moves: str):
        self.board = self.board.updateboard(moves)
        if (not(self.tree)):
            self.tree = MoveTreeNode(self.board, 0, 4, self.piececolor, self.e)
        #return None if the latest update has created a draw by repetition and ended the game
        #return True if the game is still continuing
        if (self.board.isrepetition()):
            return None
        return True
        
    #resets board, then makes every move in the provided move string
    
    def updateboardall(self, moves: str):
        self.board = self.board.updateboardall(moves)
        if (self.board.getturn() == self.piececolor):
            self.tree = MoveTreeNode(self.board, 0, 4, self.piececolor, self.e)
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
            move_stack = self.board.getmovestack()
            if (len(move_stack) > 0):
                bot_move = move_stack[-2]
                opponent_move = move_stack[-1]
                for i in self.tree.children:
                    if (i.board.getmovestack()[-1] == bot_move):
                        for j in i.children:
                            if (j.board.getmovestack()[-1] == opponent_move):
                                self.tree = j
                                self.tree.shift_depth(0)
                                break
            move = self.tree.getbestmove()
            
            return move
        else:
            return None
        
    
    def getboard(self):
        return self.board.getboard()
    

    #gets a heuristic evaluation of the board
    def shalloweval(self):
        return self.board.shalloweval(self.piececolor)