import chess
class BoardWrapper():
    def __init__(self):
        self.board = chess.Board(chess.STARTING_BOARD_FEN)
    
    def updateboard(self, moves: str):
        moves = moves.strip()
        moveslist = moves.split()
        ucimove: str = moveslist[len(moveslist) - 1]
        move = chess.Move.from_uci(ucimove)
        self.board.push(move)
        return self
