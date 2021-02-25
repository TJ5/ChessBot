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
        self.knighttable = [
            -50,-40,-30,-30,-30,-30,-40,-50, #1
            -40,-20,  0,  5,  5,  0,-20,-40, #2
            -30,  5, 10, 15, 15, 10,  5,-30, #3
            -30,  0, 15, 20, 20, 15,  0,-30, #4
            -30,  5, 15, 20, 20, 15,  5,-30, #5 
            -30,  0, 10, 15, 15, 10,  0,-30, #6
            -40,-20,  0,  0,  0,  0,-20,-40, #7 
            -50,-40,-30,-30,-30,-30,-40,-50, #8
        ]
        self.bishoptable = [
            -20,-10,-10,-10,-10,-10,-10,-20, #1
            -10,  5,  0,  0,  0,  0,  5,-10, #2
            -10, 10, 10, 10, 10, 10, 10,-10, #3
            -10,  0, 10, 10, 10, 10,  0,-10, #4
            -10,  5,  5, 10, 10,  5,  5,-10, #5            
            -10,  0,  5, 10, 10,  5,  0,-10, #6
            -10,  0,  0,  0,  0,  0,  0,-10, #7
            -20,-10,-10,-10,-10,-10,-10,-20, #8
        ]
        self.rooktable = [
            0,  0,  0,  5,  5,  0,  0,  0,  #1
            -5,  0,  0,  0,  0,  0,  0, -5, #2
            -5,  0,  0,  0,  0,  0,  0, -5, #3
            -5,  0,  0,  0,  0,  0,  0, -5, #4
            -5,  0,  0,  0,  0,  0,  0, -5, #5
            -5,  0,  0,  0,  0,  0,  0, -5, #6
            5, 10, 10, 10, 10, 10, 10,  5,  #7
            0,  0,  0,  0,  0,  0,  0,  0,  #8
        ]
        self.queentable = [
            -20,-10,-10, -5, -5,-10,-10,-20, #1
            -10,  0,  5,  0,  0,  0,  0,-10, #2
            -10,  5,  5,  5,  5,  5,  0,-10, #3
            0,  0,  5,  5,  5,  5,  0, -5,   #4
            -5,  0,  5,  5,  5,  5,  0, -5,  #5
            -10,  0,  5,  5,  5,  5,  0,-10, #6
            -10,  0,  0,  0,  0,  0,  0,-10, #7
            -20,-10,-10, -5, -5,-10,-10,-20, #8    
        ]
        self.kingtable = [
            20, 30, 10,  0,  0, 10, 30, 20,  #1
            20, 20,  0,  0,  0,  0, 20, 20,  #2
            -10,-20,-20,-20,-20,-20,-20,-10, #3
            -20,-30,-30,-40,-40,-30,-30,-20, #4
            -30,-40,-40,-50,-50,-40,-40,-30, #5
            -30,-40,-40,-50,-50,-40,-40,-30, #6
            -30,-40,-40,-50,-50,-40,-40,-30, #7
            -30,-40,-40,-50,-50,-40,-40,-30, #8
        ]
        self.kingendgametable = [
            -50,-30,-30,-30,-30,-30,-30,-50, #1
            -30,-30,  0,  0,  0,  0,-30,-30, #2
            -30,-10, 20, 30, 30, 20,-10,-30, #3
            -30,-10, 30, 40, 40, 30,-10,-30, #4
            -30,-10, 30, 40, 40, 30,-10,-30, #5
            -30,-10, 20, 30, 30, 20,-10,-30, #6
            -30,-20,-10,  0,  0,-10,-20,-30, #7
            -50,-40,-30,-20,-20,-30,-40,-50, #8
        ]
    def getpawnmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.pawntable[square]
        else:
            return self.pawntable[chess.square_mirror(square)]

    def getknightmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.knighttable[square]
        else:
            return self.knighttable[chess.square_mirror(square)]
    
    def getbishopmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.bishoptable[square]
        else:
            return self.bishoptable[chess.square_mirror(square)]
    
    def getrookmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.rooktable[square]
        else:
            return self.rooktable[chess.square_mirror(square)]
    
    def getqueenmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.queentable[square]
        else:
            return self.queentable[chess.square_mirror(square)]
    
    def getkingmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.kingtable[square]
        else:
            return self.kingtable[chess.square_mirror(square)]

    def getkingendmodifier(self, square: chess.Square, color: chess.Color):
        if (color == chess.WHITE):
            return self.kingendgametable[square]
        else:
            return self.kingendgametable[chess.square_mirror(square)]

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
        elif (piece.piece_type == chess.KNIGHT):
            val = knight
            val = val + self.getknightmodifier(square, piece.color)
        elif (piece.piece_type == chess.BISHOP):
            val = bishop
            val = val + self.getbishopmodifier(square, piece.color)
        elif (piece.piece_type == chess.ROOK):
            val = rook
            val = val + self.getrookmodifier(square, piece.color)
        elif (piece.piece_type == chess.QUEEN):
            val = queen
            val = val + self.getqueenmodifier(square, piece.color)
        elif (piece.piece_type == chess.KING):
            val = king
            endgame = False #Implement logic for if endgame or not later
            if (endgame):
                val = val + self.getkingendmodifier(square, piece.color)
            else:
                val = val + self.getkingmodifier(square, piece.color)

        #If it isn't a pawn, ignore for now
        else:
            pass
        val = val * modifier
        return val
        
