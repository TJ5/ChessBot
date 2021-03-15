import chess
import re
from value import SquareValue
class BoardWrapper():
    def __init__(self, board = chess.Board(chess.STARTING_FEN)):
        self.board : chess.Board = board
        
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
        return self.board.legal_moves
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
    def shalloweval(self, piececolor):
        eval = 0
        i = 0
        valfinder = SquareValue()
        #loop through each square of the board
        #If a piece exists, add it's value to the eval
        while (i < 64):
            piece = self.getpiece(i)
            if (piece):
                eval = eval + valfinder.getpiecevalue(i, piececolor, piece)
            i = i + 1
        return eval
    
    def getmovestack(self):
        return self.board.move_stack
