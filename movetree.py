from boardwrapper import BoardWrapper
import chess

import copy
class MoveTreeNode():
    #Move Tree node
    def __init__(self, board: BoardWrapper, movesahead: int, maxdepth: int, piececolor):
        
        self.board = board.getcopy()
        self.children = []
        self.maxdepth = maxdepth
        self.movesahead = movesahead
        self.piececolor = piececolor
        
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
            self.children.append(MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth, self.piececolor))
            
            i = i + 1
        
                
    def __str__(self):
        
        #ret = "\t"*self.movesahead + str(self.board.getmovestack()) + "\n"
        ret = "\t"*self.movesahead + str(self.board.getmovestack())  + "\n"
        for child in self.children:
            ret += child.__str__()
        return ret
    
    #returns number of leaf nodes 
    def size(self):
        counter = 0
        #if leaf node - basecase
        if (len(self.children) == 0):
            return 1
        else:
            i = 0
            while (i < len(self.children)):
                counter = counter + self.children[i].size()
                i = i + 1
        return counter

    def getbestboard(self):
        #basecase
        if (len(self.children) == 0):
            return self.board
        else:
            
            if (self.movesahead % 2 == 0): 
                i = 0
                maxchild = None
                maxeval = -20000
                while (i < len(self.children)):
                    
                    if (self.children[i].getbestboard().shalloweval(self.piececolor) >= maxeval):
                        maxeval = self.children[i].getbestboard().shalloweval(self.piececolor)
                        maxchild = self.children[i].getbestboard()
                    i = i + 1
                return maxchild
            elif (self.movesahead % 2 == 1):
                i = 0
                minchild = None
                mineval = 20000
                while (i < len(self.children)):
                    
                    if (self.children[i].getbestboard().shalloweval(self.piececolor) <= mineval):
                        mineval = self.children[i].getbestboard().shalloweval(self.piececolor)
                        minchild = self.children[i].getbestboard()
                    i = i + 1
                return minchild
    def getbestmove(self):
        bestboard = self.getbestboard()
        movestack = bestboard.getmovestack()
        f = open("log.txt", "a")
        f.write("[CURRENT POSITION]: " + self.board.getfen() + "\n")
        f.write("[EVAL AFTER MOVES]: " + str(bestboard.shalloweval(self.piececolor)))
        f.write("[MOVES FROM " + str(self.maxdepth) + " DEPTH]: ")
        i = len(self.board.getmovestack())
        while (i < len(movestack)):
            f.write(str(movestack[i]) + " ")
            
            i += 1
        
        f.write("\n\n")
        
        f.close()
        

        move = movestack[len(self.board.getmovestack())]
        
        return chess.Move.uci(move)