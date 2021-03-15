import unittest
from game import Game
import chess
from mockclient import MockClient
from bot import Bot
from value import SquareValue
from movetree import MoveTreeNode
from boardwrapper import BoardWrapper
m = MockClient()
game = Game(m, True)
game.start()
current_state = game.current_state
bot = Bot("black")
value = SquareValue()
class TestBot(unittest.TestCase):

    def test_bot_movemaking(self): 
        bot.updateboardtest("e2e4 e7e5")
        move = bot.getmove()
        self.assertFalse(move)
        bot.updateboardtest("e2e4 e7e5 g1f3")
        move = bot.getmove()
        testboard = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
        self.assertTrue(chess.Move.from_uci(move) in testboard.legal_moves)
        
        
    def test_pawn_eval(self):
        self.assertEqual(value.getpawnmodifier(chess.E4, chess.WHITE), 20)
        self.assertEqual(value.getpawnmodifier(chess.E2, chess.BLACK), 50)
     
        bot.updateboardtest("e2e4")
        self.assertEqual(bot.shalloweval(), -40)
    def test_knight_eval(self):
        bot.updateboardtest("e2e4 g8f6")
        self.assertEqual(bot.shalloweval(), 10)
    def test_bishop_eval(self):
        bot.updateboardtest("e2e4 e7e5 f1c4")
        self.assertEqual(bot.shalloweval(), -20)
    def test_castle_eval(self): #evaluates a castling move to test rooks and king middlegame piece-square tables
        
        
        bot.updateboardtest("e2e4 e7e5 d2d4 d7d5 f1d3 f8d6 c1e3 c8e6 d1d2 d8d7 b1c3 b8c6 g1f3")
        
        self.assertTrue(bot.getboard().find_move(60, 58))
        
        
    def test_game_init(self):
        self.assertEqual(current_state["type"], "gameFull")
        self.assertEqual(current_state["white"]["id"], "whenchess")
    def test_event_loop_moves(self):
        self.assertTrue(chess.Move.from_uci(m.moves[0]))
        self.assertTrue(chess.Move.from_uci(m.moves[1]))
    
    def test_movetree(self):
        board = BoardWrapper(chess.Board("r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 1 5"))
        tree = MoveTreeNode(board, 0, 3)
        print(tree)
    

unittest.main()