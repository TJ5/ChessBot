import unittest
from game import Game
import chess
from mockclient import MockClient
from bot import Bot
m = MockClient()
game = Game(m, True)
game.start()
current_state = game.current_state
bot = Bot("black")
class TestBot(unittest.TestCase):

    def test_bot_movemaking(self): 
        move = bot.updateboardtest("e2e4 e7e5")
        self.assertFalse(move)
        move = bot.updateboardtest("e2e4 e7e5 g1f3")
        testboard = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
        self.assertTrue(chess.Move.from_uci(move) in testboard.legal_moves)
    def test_game_init(self):
        self.assertEqual(current_state["type"], "gameFull")
        self.assertEqual(current_state["white"]["id"], "whenchess")
    def test_event_loop_moves(self):
        self.assertTrue(chess.Move.from_uci(m.moves[0]))
        self.assertTrue(chess.Move.from_uci(m.moves[1]))
    
    
unittest.main()