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
        
        
    def addchildren(self, timer_event, alpha, beta, previous_movestack=None):
        
        table_lookup = self.TTable.get(self.board.board)
        hash_move = None
        
        while not timer_event.is_set():
            if table_lookup:
                #position found in hash table
                if table_lookup[0] == self.board.get_board_fen() and table_lookup[3] == self.board.getturn():
                    if table_lookup[2] >= (self.maxdepth - self.movesahead): #hashed depth is sufficent in completing the search to maxdepth or greater
                        bestboard = BoardWrapper(self.e, chess.Board(table_lookup[0]))
                        bestboard.board.turn = table_lookup[3]
                        bestboard.board.move_stack = self.board.board.move_stack.copy()
                        i = len(table_lookup[1]) - table_lookup[2]
                        while (i < len(table_lookup[1])):
                            bestboard.pushmove(table_lookup[1][i])
                            i += 1
                            
                        return bestboard
                    else:
                        if len(table_lookup[1]) >= (self.movesahead + 1):
                            hash_move = table_lookup[1][self.movesahead]
            previous_move = None
            #if previous_movestack:
            #    compare = previous_movestack[:self.movesahead]
            #    if compare == self.board.getmovestack():
            #        if len(previous_movestack) > len(self.board.getmovestack()[-self.movesahead:]):
            #            previous_move = previous_movestack[self.movesahead]
            if previous_movestack:
                last_len = len(previous_movestack)
            else:
                last_len = -1
            if (last_len > (self.movesahead)):
                previous_move = previous_movestack[self.movesahead]
            
            moves = self.board.getsortedmoves(hash_move, previous_move) 
            
            
            
            
            if (len(moves) == 0 or self.movesahead == self.maxdepth):
                return self.board
                
            else:
                
                best_child = None
                best_eval = (-1 * math.inf) if self.movesahead % 2 == 0 else math.inf
                for i in moves:
                    if not timer_event.is_set():
                        childboard = BoardWrapper(self.e)
                        childboard.board = self.board.board.copy() 
                        childboard.pushmove(i)
                        childnode = MoveTreeNode(childboard, self.movesahead + 1, self.maxdepth, self.piececolor, self.e, self.TTable)
                        self.children.append(childnode)
                        board : BoardWrapper = childnode.addchildren(timer_event, alpha, beta, previous_movestack)
                        if board:
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
                    else:
                        return
                if (self.maxdepth - self.movesahead == 2):
                    if best_child:
                        #hash positions at 2 plies from leaves
                        movestack = best_child.getmovestack()
                        difference = len(movestack) - len(self.board.getmovestack())
                        best_child_movesahead = difference + self.movesahead
                        #difference in most cases will be 2, but could be less if the game ends
                        
                        self.TTable.put(self.board.board, movestack[-1*best_child_movesahead:], difference)    
                return best_child
        return    
                
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
    def size(self, max=None):
        if not max:
            max = self.maxdepth
        counter = 0
        #if leaf node - basecase
        if (len(self.children) == 0 or self.movesahead == max):
            return 1
        else:
            i = 0
            while (i < len(self.children)):
                counter = counter + self.children[i].size(max)
                i = i + 1
        return counter

    
        
    def getbestmove(self, timer_event):
        print("GET BEST MOVE CALLED")
        
        now = time.time()
        
        
        self.maxdepth = 1
        bestboard = None 
        move = None
        current_best = None
        while not timer_event.is_set():
            

            if move:
                diff = len(bestboard.getmovestack()) - len(self.board.getmovestack()) 
                #mostly self.maxdepth, but we calculate it to compensate for the chance it is less if the game ends
                current_best : BoardWrapper = self.addchildren(timer_event, (-1 * math.inf), math.inf, previous_movestack=bestboard.getmovestack()[-diff:])
            else:
                current_best : BoardWrapper = self.addchildren(timer_event, -1 * math.inf, math.inf)
            if current_best:
                print(str(current_best.getmovestack()))
                
                #bestboard is the var to be returned, and only stores searches which have been completed.
                bestboard = current_best
                move = bestboard.getmovestack()[len(self.board.getmovestack())]
                self.maxdepth += 1
            
        print('set')
        search_time = time.time() - now
        
        is_endgame : bool = bestboard.is_endgame()
        movestack = bestboard.getmovestack()
        depth = len(movestack) - len(self.board.getmovestack())
        s = self.size(depth)
        f = open("log.txt", "a")
        f.write("[TIME THIS MOVE]: " + str(search_time) + " [TIME PER NODE]: " + str(search_time/s) + "\n")
        f.write("[LEAVES SEARCHED]: " + str(s) + "\n")
        f.write("[CURRENT POSITION]: " + self.board.getfen() + "\n")
        f.write("[IS ENDGAME]: " + str(is_endgame) + "\n")
        f.write("[EVAL AFTER MOVES]: " + str(bestboard.shalloweval(self.piececolor)))
        f.write("[MOVES FROM " + str(depth) + " DEPTH]: ")
        i = len(self.board.getmovestack())
        while (i < len(movestack)):
            f.write(str(movestack[i]) + " ")
            
            i += 1
        
        f.write("\n\n")
        
        f.close()
        

        move = movestack[len(self.board.getmovestack())]
        
        return chess.Move.uci(move)