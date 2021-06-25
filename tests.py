from endgame import EndgamePredictor
import unittest
from game import Game
import chess
from mockclient import MockClient
from bot import Bot
from value import SquareValue
from movetree import MoveTreeNode
from boardwrapper import BoardWrapper
from table import TTable
import math
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
    
        
    def test_table(self):
        t = TTable()
        e = EndgamePredictor()
        b = BoardWrapper(e)
        tree = MoveTreeNode(b, 0, 4, chess.WHITE, e)
        bestboard = tree.addchildren((-1 * math.inf), math.inf)
        t.put(b.board,bestboard.getmovestack(), 4)
        self.assertEqual(t.table[5060803636482931868], ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', [chess.Move.from_uci('g1f3'), chess.Move.from_uci('g8f6'), chess.Move.from_uci('b1c3'), chess.Move.from_uci('b8c6')], 4])
        self.assertEqual(t.get(b.board)[1][0], chess.Move.from_uci('g1f3'))
    
         
    def test_tree_table_lookup(self):
        #t = TTable()
        e = EndgamePredictor()
        b = BoardWrapper(e)
        tree = MoveTreeNode(b, 0, 4, chess.WHITE, e)
        
        tree.getbestmove()
        s = tree.size()
        print(str(s))
        self.assertLess(s, 3346)

    
unittest.main()