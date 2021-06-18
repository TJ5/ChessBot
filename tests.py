import unittest
from game import Game
import chess
from mockclient import MockClient
from bot import Bot
from value import SquareValue
from movetree import MoveTreeNode
from boardwrapper import BoardWrapper
from endgame import EndgamePredictor
class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        
        self.bot = Bot("black")
        self.value = SquareValue()
    def test_game_init(self):
        m = MockClient()
        game = Game(m, True)
        
        game.start()
        game.join()
        current_state = game.current_state
        self.assertEqual(current_state["type"], "gameFull")
        self.assertEqual(current_state["white"]["id"], "whenchess")
        
        self.assertTrue(m.moves[0])
        self.assertTrue(m.moves[1])
        self.assertEqual(m.moves[2], "c3d5")
        
    def test_bot_movemaking(self): 
        self.bot.updateboardall("e2e4 e7e5")
        move = self.bot.getmove()
        self.assertFalse(move)
        self.bot.updateboardall("e2e4 e7e5 g1f3")
        move = self.bot.getmove()
        testboard = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
        self.assertTrue(chess.Move.from_uci(move) in testboard.legal_moves)
        
        
    def test_pawn_eval(self):
        self.assertEqual(self.value.getpawnmodifier(chess.E4, chess.WHITE), 20)
        self.assertEqual(self.value.getpawnmodifier(chess.E2, chess.BLACK), 50)
     
        self.bot.updateboardall("e2e4")
        self.assertEqual(self.bot.shalloweval(), -40)
    def test_knight_eval(self):
        self.bot.updateboardall("e2e4 g8f6")
        self.assertEqual(self.bot.shalloweval(), 10)
    def test_bishop_eval(self):
        self.bot.updateboardall("e2e4 e7e5 f1c4")
        self.assertEqual(self.bot.shalloweval(), -20)
    

    def test_tree_recycle(self):
        e = EndgamePredictor()
        bw = BoardWrapper(e, chess.Board("R6R/1r3pp1/6kp/3pPp2/1r2q1P1/7P/1P1Q3K/8 w - - 0 1"))
        tree = MoveTreeNode(bw, 0, 2, chess.WHITE, e)
        tree.getbestmove()
        tree.shift_depth(0)
        tree.shift_max_depth(4)
        move = tree.getbestmove()
        self.assertEqual(move, "d2h6")
    
    
    
        
    
        
    

unittest.main()