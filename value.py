import chess
class SquareValue():
    def __init__(self):
        #These are tables of number modifiers in centipawns (hundreths of pawns)
        #Each number represents the modifier of a piece on a given square, starting from a1, to a2, ending on h8
        #Depending on a piece's location, it's value will generally change
        #Tables are from white's perspective
        self.pawntable = [
        #a  b   c   d   e   f   g   h
        0,  0,  0,  0,  0,  0,  0,  0,  #1
        5, 10, 10,-20,-20, 10, 10,  5,  #2
        5, -5,-10,  0,  0,-10, -5,  5,  #3
        0,  0,  0, 20, 20,  0,  0,  0,  #4
        5,  5, 10, 25, 25, 10,  5,  5,  #5
        10, 10, 20, 30, 30, 20, 10, 10, #6
        50, 50, 50, 50, 50, 50, 50, 50, #7
        0,  0,  0,  0,  0,  0,  0,  0   #8
        ]
    def getpawnmodifier(self, square: chess.Square, color: chess.Color):
        #Return the index of the pawntable array that is the requested square
        #If black, mirror the square first
        
        if (color == chess.WHITE):
            return self.pawntable[square]
        else:
            return self.pawntable[chess.square_mirror(square)]
    def getpiecevalue(self, square:chess.Square, color: chess.Color, piece: chess.Piece):
        val = 0
        
        #default piece values
        pawn = 100
        knight = 320
        bishop = 330
        rook = 500
        queen = 900
        king = 20000

        #if the piece color and the bot's colors are different, it has a negative evaluation
        modifier = 1
        if (color and piece.color) or ((not color) and (not piece.color)):
            modifier = 1
        else:
            modifier = -1
        
        #add modifiers based on what square the pawn is on
        if (piece.piece_type == chess.PAWN):
            val = pawn
            val = val + self.getpawnmodifier(square, piece.color)
        #If it isn't a pawn, ignore for now
        else:
            pass
        val = val * modifier
        return val
        
