import threading
from mockstream import MockStream
from bot import Bot
import berserk
class Game(threading.Thread):
    def __init__(self, test_mode: bool, client: berserk.Client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        if test_mode == False:
            self.stream = client.bots.stream_game_state(game_id)
        else: #testing
            m = MockStream()
            self.stream = m.stream()
        #initialize two fields for whose turn it is and the bots piece color
        self.botpieces = "white"
        
        #define their values
        self.current_state = next(self.stream)
        if (not (self.current_state['white']['id'] == 'whenchess')):
            self.botpieces = "black"
            
        #intialize a bot object to pass board state to
        self.bot = Bot(self.botpieces)
    
    
    def run(self):
        if (self.botpieces == "white"):
            self.handle_state_change(self.current_state['state'])
        for event in self.stream:
            print(event)
            if event['type'] == 'gameState':
                
                
                self.handle_state_change(event)
                
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    
    
    def handle_state_change(self, game_state):
        if ((game_state['status'] == 'created') or (game_state['status'] == 'started')): #game in progress
            #logic here to be implemented on when to accept draws
            move = self.bot.updateboard(game_state["moves"])
            if (move):
                self.makemove(move)
            else:
                return

        else:
            print("game end")
            pass

    def handle_chat_line(self, chat_line):
        #ignoring chat for now
        pass
    def makemove(self, move: str):
        self.client.bots.make_move(self.game_id, move)
    