import chess
class BoardWrapper():
    def __init__(self):
        self.board = chess.Board(chess.STARTING_BOARD_FEN)
        self.board.turn = chess.WHITE
    def updateboard(self, moves: str):
        if(moves):
            moves = moves.strip()
            moveslist = moves.split()
            ucimove: str = moveslist[len(moveslist) - 1]
            move = chess.Move.from_uci(ucimove)
            self.board.push(move)
        #do nothing if moves is empty / it is move 1
        return self
    def getmove(self):
        return next(self.board.generate_legal_moves())
    def getturn(self):
        return self.board.turn
    def getfen(self):
        return self.board.fen()
