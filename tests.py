import unittest
from game import Game
game = Game(True, True, True)
current_state = game.current_state
gameState = next(game.stream)
class TestBot(unittest.TestCase):

    def test_game_init(self):
        self.assertEqual(current_state["type"], "gameFull")
        self.assertEqual(current_state["white"]["id"], "whenchess")
    def test_game_move1(self):
        self.assertEqual(gameState["moves"], "e2e4 e7e5")
        self.assertEqual(gameState["type"], "gameState")
        
    def test_game_move3(self):
        gameState = next(game.stream)
        self.assertEqual(gameState["moves"], "e2e4 e7e5 d1f3 g8c6 f1c4 d7d6 f3f7")
        
        
unittest.main()