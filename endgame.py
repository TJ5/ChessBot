import pandas as pd
from sklearn.naive_bayes import GaussianNB

import chess
import numpy as np
from value import SquareValue
class EndgamePredictor():
    def __init__(self):
        data = pd.read_csv('CheckEndgame.csv')
        data["Pieces"] = data.apply(lambda row: self.gettotalpieces(chess.Board(row["FEN"])), axis=1)
        data["Material"] = data.apply(lambda row: self.gettotalmaterial(chess.Board(row["FEN"])), axis=1)
        data["Major Pieces"] = data.apply(lambda row: self.getmajorpieces(chess.Board(row["FEN"])), axis=1)

        x = data[['Pieces', 'Material', 'Major Pieces']]
        y = data.Endgame

        self.model = GaussianNB()
        self.model.fit(x, y)
    def is_endgame(self, fen : str):
        board = chess.Board(fen)
        arr = np.array([self.gettotalpieces(board), self.gettotalmaterial(board), self.getmajorpieces(board)])
        result = self.model.predict(arr.reshape(-1, 1))
        if (result.any()):
            return True
        else:
            return False
    def gettotalmaterial(self, board : chess.Board):
        i = 0
        valfinder = SquareValue()
        material = 0
        while (i < 64):
            piece = board.piece_at(i)
            if (piece):
                if ((piece.piece_type > 1) and (piece.piece_type < 6)):
                    material += abs(valfinder.getpiecevalue(i, chess.WHITE, piece, True))
            i += 1
        return material
    def gettotalpieces(self, board : chess.Board):
        i = 0
        pieces = 0
        while (i < 64):
            piece = board.piece_at(i)
            if (piece):
                pieces += 1
            i += 1
        return pieces - 2
    def getmajorpieces(self, board : chess.Board):
        i = 0
        pieces = 0
        while (i < 64):
            piece = board.piece_at(i)
            if (piece):
                if ((piece.piece_type > 1) and (piece.piece_type < 6)):
                    pieces += 1
            i += 1
        return pieces