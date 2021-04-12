import chess
import re
from value import SquareValue
import copy
class BoardWrapper():
    def __init__(self, board = chess.Board(chess.STARTING_FEN), drawclaimed = False):
        self.board : chess.Board = board
        self.draw = drawclaimed
        
    #given a string of every move, push the latest one to update the board
    def updateboard(self, moves: str):
        if(moves):
            moves = moves.strip()
            moveslist = moves.split()
            ucimove: str = moveslist[len(moveslist) - 1]
            move = chess.Move.from_uci(ucimove)
            self.board.push(move)
        #do nothing if moves is empty / it is move 1
        return self
    
    #some helper methods
    def getmoves(self):
        if (not self.draw):
            return self.board.legal_moves
        else:
            return []
    def getturn(self):
        return self.board.turn
    def getfen(self):
        return self.board.fen()
    def getboard(self):
        return self.board
    def isrepetition(self):
        return self.board.is_repetition(5)
    def getpiece(self, square):
        return self.board.piece_at(square)
    #for testing only, given a string of every move, reset the board and push all of them
    def updateboardtest(self, moves: str):
        if(moves):
            moves = moves.strip()
            self.board.reset()
            movelist = re.compile('\w+').findall(moves)
            i = 0
            while (i < len(movelist)):
                self.board.push(chess.Move.from_uci(movelist[i]))
                i+=1
                
        return self

    #pushes a move to the board stack
    def pushmove(self, move : chess.Move):
        self.board.push(move)
        return self
    def popmove(self):
        return self.board.pop()
    def drawable(self):
        return self.board.can_claim_draw()
    def shalloweval(self, piececolor):
        if (self.draw):
            return 0
        
        eval = 0
        
        valfinder = SquareValue()
        #loop through each square of the board
        #If a piece exists, add it's value to the eval
        outcome = self.board.outcome(claim_draw = False)
        if (outcome):
            if (outcome.winner):
                if (outcome.winner == piececolor): #bot wins
                    eval = 20000
                else: #opponent wins
                    eval = -20000
            else:
                eval = 0
        else:
            i = 0
            while (i < 64):
                piece = self.getpiece(i)
                if (piece):
                    value = valfinder.getpiecevalue(i, piececolor, piece)
                    eval += value
                    if ((piece.piece_type > 1) and piece.piece_type < 6):
                        if (piece.color == piececolor):
                            attackers = list(self.board.attackers((not(piece.color)), chess.parse_square(chess.square_name(i))))
                            
                            j = 0
                            while (j < len(attackers)):
                                att = abs(valfinder.getpiecevalue(attackers[j], piececolor, self.board.piece_at(attackers[j])))
                                if (abs(value - att) >= 100):
                                    eval -= value
                                    break
                                j += 1
                    
                i = i + 1
        return eval
    
    def getmovestack(self):
        return self.board.move_stack.copy()
    def getcopy(self):
        return copy.copy(self)