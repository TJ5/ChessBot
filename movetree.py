from boardwrapper import BoardWrapper
import chess
from bot import Bot
import copy
class MoveTreeNode():
    #Move Tree node
    def __init__(self, board: BoardWrapper, movesahead: int, maxdepth: int):
        
        self.board = board.getcopy()
        self.children = []
        self.maxdepth = maxdepth
        self.movesahead = movesahead
        if (movesahead < maxdepth):
            self.addchildren()
    def addchildren(self):
        #To be optimized later
        #For now, add child boards for each legal board state that may occur
        moves = list(self.board.getmoves()) 
        i = 0
        childboard = BoardWrapper()
        while (i < len(moves)):
            #set childboard's board field to a shallow copy of the parent boardwrapper's board field
            childboard.board = self.board.board.copy() 
            childboard.pushmove(moves[i])
            self.children.append(MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth))
            
            i = i + 1
        
                
    def __str__(self):
        
        ret = "\t"*self.movesahead + self.board.getfen() + "\n"
        for child in self.children:
            ret += child.__str__()
        return ret