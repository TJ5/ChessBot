import chess
import re
class BoardWrapper():
    def __init__(self):
        self.board = chess.Board(chess.STARTING_BOARD_FEN)
        self.board.turn = chess.WHITE
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
    def getmove(self):
        return next(self.board.generate_legal_moves())
    def getturn(self):
        return self.board.turn
    def getfen(self):
        return self.board.fen()
    def getboard(self):
        return self.board
    def isrepetition(self):
        return self.board.is_repetition(5)
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