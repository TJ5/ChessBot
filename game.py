import threading
from mockstream import MockStream
import berserk
class Game(threading.Thread):
     def __init__(self, test_mode, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        if test_mode == False:
            self.stream = client.bots.stream_game_state(game_id)
        else: #testing
            m = MockStream()
            self.stream = m.stream()
            
        self.current_state = next(self.stream)

     def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

     def handle_state_change(self, game_state):
        print(game_state)
        pass

     def handle_chat_line(self, chat_line):
        pass