from boardwrapper import BoardWrapper
import chess
import math
import time
from table import TTable
class MoveTreeNode():
    #Move Tree node
    def __init__(self, board: BoardWrapper, movesahead: int, maxdepth: int, piececolor, e, *args):
        
        self.board = board.getcopy()
        self.children = []
        self.maxdepth = maxdepth
        self.movesahead = movesahead
        self.piececolor = piececolor
        self.e = e
        
        if args:
            self.TTable = args[0]
        else:
            self.TTable = TTable()
        
        
    def addchildren(self, alpha, beta):
        table_lookup = self.TTable.get(self.board.board)
        if table_lookup:
            #position found in hash table
            if table_lookup[0] == self.board.getfen():
                if table_lookup[2] >= (self.maxdepth - self.movesahead): #hashed depth is sufficent in completing the search to maxdepth or greater
                    bestboard = BoardWrapper(self.e, chess.Board(table_lookup[0]))
                    i = self.maxdepth
                    while i > 0:
                        if (i > table_lookup[2]): 
                            bestboard.board.move_stack.append(table_lookup[1][-i])
                        else:
                            bestboard.pushmove(table_lookup[1][-i])
                        i -= 1
                    return bestboard
        
        moves = self.board.getsortedmoves(self.piececolor) 
        
        
        #if (childboard.drawable()):
        #    drawboard = BoardWrapper(chess.Board, True)
        #    drawboard.board = childboard.board.copy()
        #    self.children.append(MoveTreeNode(drawboard, self.movesahead + 1, self.maxdepth, self.piececolor))
        
        if (len(moves) == 0 or self.movesahead == self.maxdepth):
            return self.board
            
        else:
            
            best_child = None
            best_eval = (-1 * math.inf) if self.movesahead % 2 == 0 else math.inf
            for i in moves:
                childboard = BoardWrapper(self.e)
                childboard.board = self.board.board.copy() 
                childboard.pushmove(i)
                childnode = MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth, self.piececolor, self.e, self.TTable)
                self.children.append(childnode)
                board : BoardWrapper = childnode.addchildren(alpha, beta)
                eval = board.shalloweval(self.piececolor)
                if (self.movesahead % 2 == 0 and eval > best_eval) or (self.movesahead % 2 == 1 and eval < best_eval):
                    best_eval = eval
                    best_child = board
                elif (eval == best_eval):
                    if (len(board.getmovestack()) < len(best_child.getmovestack())):
                        best_child = board
                    else:
                        pass
                if (self.movesahead % 2 == 0):
                    alpha = max(alpha, best_eval)
                else:
                    beta = min(beta, best_eval)
                if (alpha >= beta):
                    break #prune branch
            if (self.movesahead == 2):
                #hash positions at depth 2
                self.TTable.put(self.board.board, best_child.getmovestack(), self.movesahead)    
            return best_child
            
                
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