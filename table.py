from boardwrapper import BoardWrapper
import chess.polyglot
import chess

class TTable():
    def __init__(self):
        self.table = {}
        
        

        
    def hash(self, board : chess.Board):
        return chess.polyglot.zobrist_hash(board)
    def put(self, board : chess.Board, move_stack, value : int, is_bound : int, depth : int):
        val = self.hash(board)
        fen = board.fen()

        #if an entry already exists in the table for the given hash key, 
        #check if it is the same position or not. If it is, overwrite it if the new entry is at a higher depth.
        #if it is not, overwrite it.

        if val in self.table:
            if self.table[val][0] == fen:
                if self.table[val][depth] < depth:
                    self.table[val] = [fen, move_stack, value, is_bound, depth]
                    return
                else:
                    return
        
        self.table[val] = [fen, move_stack, value, is_bound, depth]
    def get(self, board : chess.Board):
        val = self.hash(board)
        if val in self.table:
            return self.table[val]
        return None
    
    
