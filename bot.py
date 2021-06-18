from boardwrapper import BoardWrapper
import chess
from movetree import MoveTreeNode
from endgame import EndgamePredictor
class Bot():
    def __init__(self, piececolor: str, fen = chess.STARTING_FEN):
        self.e = EndgamePredictor()
        self.board = BoardWrapper(self.e, chess.Board(fen))
        self.piececolor = piececolor
        self.tree = None
        if (self.piececolor == "white"):
            self.piececolor = chess.WHITE
            tboard = BoardWrapper(self.e)
            tboard.board = self.board.board.copy()
            self.tree = MoveTreeNode(tboard, 0, 4, chess.WHITE, self.e)
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
            if (not(self.tree)):
                # construct tree if bot plays black on its first move
                self.tree = MoveTreeNode(self.board, 0, 4, chess.BLACK, self.e)
            else:
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
                                    move = self.tree.getbestmove()
                                    return move
                    #a working tree exists, but the current board position is not in it
                    tree_board = BoardWrapper(self.e)
                    tree_board.board = self.board.board.copy()
                    self.tree = MoveTreeNode(tree_board, 0, 4, self.piececolor, self.e)
                        
            move = self.tree.getbestmove()
            return move
        else:
            return None
        
    
    def getboard(self):
        return self.board.getboard()
    

    #gets a heuristic evaluation of the board
    def shalloweval(self):
        return self.board.shalloweval(self.piececolor)