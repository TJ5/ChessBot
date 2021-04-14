from boardwrapper import BoardWrapper
import chess
import math
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
        moves = self.board.getsortedmoves() 
        i = 0
        childboard = BoardWrapper()
        while (i < len(moves)):
            #set childboard's board field to a shallow copy of the parent boardwrapper's board field
            childboard.board = self.board.board.copy() 
            childboard.pushmove(moves[i])
            self.children.append(MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth, self.piececolor))
            #if (childboard.drawable()):
            #    drawboard = BoardWrapper(chess.Board, True)
            #    drawboard.board = childboard.board.copy()
            #    self.children.append(MoveTreeNode(drawboard, self.movesahead + 1, self.maxdepth, self.piececolor))
            i = i + 1
        
                
    def __str__(self):
        
        #ret = "\t"*self.movesahead + str(self.board.getmovestack()) + "\n"
        ret = ""
        i = 0
        moves = self.board.getmovestack()
        while (i < len(moves)):
            moves[i] = chess.Move.uci(moves[i])
            i += 1
        if (len(self.board.getmovestack())):
            ret = "\t"*self.movesahead + str(moves[(-1 * (self.movesahead + 1)) : len(moves)])
            
            ret = ret + " " + str(self.board.shalloweval(self.piececolor))
            ret += "\n"
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

    def minimax(self, alpha : int, beta : int):
        #basecase
        if (len(self.children) == 0):
            return self.board
            
        else:
            if (self.movesahead % 2 == 0): 
                maxchild = None
                maxeval = (-1 * math.inf)
                for i in self.children:
                    board : BoardWrapper = i.minimax(alpha, beta)
                    if (board.shalloweval(self.piececolor) >= maxeval):
                        maxeval = board.shalloweval(self.piececolor)
                        maxchild = board
                    alpha = max(alpha, maxeval)
                    if (alpha > beta):
                        break #prune branch
                return maxchild
            elif (self.movesahead % 2 == 1):
                i = 0
                minchild = None
                mineval = math.inf
                for i in self.children:
                    board : BoardWrapper = i.minimax(alpha, beta)
                    if (board.shalloweval(self.piececolor) <= mineval):
                        mineval = board.shalloweval(self.piececolor)
                        minchild = board
                    beta = min(beta, mineval)
                    if (beta < alpha):
                        break #prune branch
                
                return minchild
    def getbestmove(self):
        bestboard : BoardWrapper = self.minimax((-1 * math.inf), math.inf)
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