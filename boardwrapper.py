import chess
import re
from value import SquareValue
import copy


import numpy as np
class BoardWrapper():
    def __init__(self, e, board = chess.Board(chess.STARTING_FEN), drawclaimed = False):
        self.board : chess.Board = board
        self.draw = drawclaimed
        self.e = e
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
    def updateboardall(self, moves: str):
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
        is_endgame = self.e.is_endgame(self.getfen())
        valfinder = SquareValue()
        #loop through each square of the board
        #If a piece exists, add it's value to the eval
        outcome = self.board.outcome(claim_draw = False)
        if (outcome):
            if (outcome.winner == piececolor): #bot wins
                eval = 20000
            elif (outcome.winner == (not piececolor)): #opponent wins
                eval = -20000
            else:
                eval = 0
        else:
            i = 0
            while (i < 64):
                piece = self.getpiece(i)
                if (piece):
                    value = valfinder.getpiecevalue(i, piececolor, piece, is_endgame)
                    eval += value
                    if ((piece.piece_type > 1) and piece.piece_type < 6):
                        if (piece.color != self.board.turn):
                            attackers = list(self.board.attackers((not(piece.color)), chess.parse_square(chess.square_name(i))))
                            #defenders = list(self.board.attackers((piece.color), chess.parse_square(chess.square_name(i))))
                            j = 0
                            while (j < len(attackers)):
                                #if len(defenders) == 0:
                                #    eval -= value
                                #    break
                                att = abs(valfinder.getpiecevalue(attackers[j], piececolor, self.board.piece_at(attackers[j]), is_endgame))
                                if (abs(value) > att): 
                                    if (abs(value) - abs(att) >= 100):
                                        eval -= value
                                        break
                                j += 1
                    
                i = i + 1
        return eval
    
    def getmovestack(self):
        return self.board.move_stack.copy()
    def getcopy(self):
        return copy.copy(self)
    def getsortedmoves(self, piececolor):
        promotions = []
        
        captures = []
        others = []
        valfinder = SquareValue()
        moves = list(self.getmoves())
        max_victim = 0
        min_aggressor = 5
        best_capture = None
        for i in moves:
            attackedpiece = self.getpiece(i.to_square)
            movedpiece = self.getpiece(i.from_square)
            
            if (i.promotion):
                promotions.append(i)
            elif (attackedpiece):
                victim_value = attackedpiece.piece_type
                aggressor_value = movedpiece.piece_type
                if (victim_value - aggressor_value) > (max_victim - min_aggressor):
                    if best_capture:
                        captures.append(best_capture)
                    best_capture = i
                    max_victim = victim_value
                    min_aggressor = aggressor_value

                else:
                    captures.append(i)
            else:
                others.append(i)
        
        if (best_capture):
            promotions.append(best_capture) # inserting the best capture before the other captures
        sorted = promotions + captures + others
       
        return sorted
    
    
    def is_endgame(self):
        return self.e.is_endgame(self.getfen())