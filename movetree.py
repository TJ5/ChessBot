from boardwrapper import BoardWrapper
import chess
import math
import time
class MoveTreeNode():
    #Move Tree node
    def __init__(self, board: BoardWrapper, movesahead: int, maxdepth: int, piececolor, e):
        
        self.board = board.getcopy()
        self.children = []
        self.maxdepth = maxdepth
        self.movesahead = movesahead
        self.piececolor = piececolor
        self.e = e
        
        
        
    def addchildren(self, alpha, beta):
        moves = self.board.getsortedmoves() 
        i = 0

        #remove moves which already exist in the tree
        for k in self.children:
            while i < len(moves):
                if k.board.getmovestack()[-1] == i:
                    moves.pop(i)
                i += 1
        
        #if (childboard.drawable()):
        #    drawboard = BoardWrapper(chess.Board, True)
        #    drawboard.board = childboard.board.copy()
        #    self.children.append(MoveTreeNode(drawboard, self.movesahead + 1, self.maxdepth, self.piececolor))
        
        if (len(moves) == 0 or self.movesahead == self.maxdepth):
            return self.board
        
        else:
            k = len(self.children)
            i = 0
            j = len(moves)
            if (self.movesahead % 2 == 0): 
                maxchild = None
                maxeval = (-1 * math.inf)
                while (i < (k + j)):
                    if (i < len(moves)):
                        childboard = BoardWrapper(self.e)
                        childboard.board = self.board.board.copy() 
                        childboard.pushmove(moves[i])
                        childnode = MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth, self.piececolor, self.e)
                        self.children.append(childnode)
                        
                    else:
                        childnode = self.children[i - j]

                    board : BoardWrapper = childnode.addchildren(alpha, beta)

                    eval = board.shalloweval(self.piececolor)
                    if (eval > maxeval):
                        maxeval = board.shalloweval(self.piececolor)
                        maxchild = board
                    elif (eval == maxeval):
                        if (len(board.getmovestack()) < len(maxchild.getmovestack())):
                            maxchild = board
                        else:
                            pass
                    alpha = max(alpha, maxeval)
                    if (alpha > beta):
                        break #prune branch
                    i += 1
                return maxchild
            elif (self.movesahead % 2 == 1):
                i = 0
                minchild = None
                mineval = math.inf
                while (i < (k + j)):
                    if (i < len(moves)):
                        childboard = BoardWrapper(self.e)
                        childboard.board = self.board.board.copy() 
                        childboard.pushmove(moves[i])
                        childnode = MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth, self.piececolor, self.e)
                        self.children.append(childnode)
                        
                    else:
                        childnode = self.children[i - j]

                    board : BoardWrapper = childnode.addchildren(alpha, beta)

                    eval = board.shalloweval(self.piececolor)
                    if (eval < mineval):
                        mineval = board.shalloweval(self.piececolor)
                        minchild = board
                    elif (eval == mineval): #if the two evaluations are the same, favor the board with a shorter movestack, if applicable
                        if (len(board.getmovestack()) < len(minchild.getmovestack())):
                            minchild = board
                        else:
                            pass
                    beta = min(beta, mineval)
                    if (beta < alpha):
                        break #prune branch
                    i += 1
                return minchild
                
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

    
        
    def getbestmove(self):
        now = time.time()
        bestboard : BoardWrapper = self.addchildren((-1 * math.inf), math.inf)
        t = time.time() - now
        s = self.size()
        is_endgame : bool = bestboard.is_endgame()
        movestack = bestboard.getmovestack()
        f = open("log.txt", "a")
        f.write("[TIME THIS MOVE]: " + str(t) + " [TIME PER NODE]: " + str(t/s) + "\n")
        f.write("[LEAVES SEARCHED]: " + str(s) + "\n")
        f.write("[CURRENT POSITION]: " + self.board.getfen() + "\n")
        f.write("[IS ENDGAME]: " + str(is_endgame) + "\n")
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

    def shift_depth(self, depth):
        self.movesahead = depth
        for i in self.children:
            i.shift_depth(depth + 1)

    def shift_max_depth(self, max):
        self.maxdepth = max
        for i in self.children:
            i.shift_max_depth(max)