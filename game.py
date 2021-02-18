import threading
from bot import Bot

from mockclient import MockClient
class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client

        #set stream to test stream or lichess stream
        #initialize test_mode var to know where to make moves
        if (isinstance(client, MockClient)):
            self.stream = client.stream()
            self.test_mode = True
        else: #set stream to lichess game event stream
            self.stream = client.bots.stream_game_state(game_id)
            self.test_mode = False
        
        #define variable to store which side the bot plays
        self.botpieces = "white"
        self.current_state = next(self.stream) #stores JSON on all pertinent info to the game on start
        if (not (self.current_state['white']['id'] == 'whenchess')):
            self.botpieces = "black"
            
        #intialize a bot object to pass board state to
        self.bot = Bot(self.botpieces)
    
    
    def run(self):
        #play the first move if white
        if (self.botpieces == "white"):
            self.handle_state_change(self.current_state['state'])
        #event loop for game state updates
        for event in self.stream:
            
            if event['type'] == 'gameState':

                game_running = self.handle_state_change(event)
                if not (game_running):
                    return
                
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    
    #Handle any game state change 
    #Returns False if game has ended, True if game continues but it is not the bot's turn, and returns the move made if applicable.
    def handle_state_change(self, game_state):
        
        if ((game_state['status'] == 'created') or (game_state['status'] == 'started')): #game in progress
            #logic here to be implemented on when to accept draws

            
            #if test mode, support inputting an arbitrary position
            if (self.test_mode):
                gamecont = self.bot.updateboardtest(game_state["moves"])
                
            else:
                gamecont = self.bot.updateboard(game_state["moves"])
            
            #get a uci string move from bot.py
            if (gamecont):
                move = self.bot.getmove()
            else:
                print("draw made")
                return False
            #make move if it is bot's turn, null move is ignored if not
            if (move):
                self.makemove(move)
                return move
            else:
                return True

        else: #game has ended
            print("game end")
            return False

    def handle_chat_line(self, chat_line):
        #ignoring chat for now
        pass
    #passes uci strings to lichess
    def makemove(self, move: str):
        if not (self.test_mode):
            self.client.bots.make_move(self.game_id, move) 
        else: 
            self.client.makemockmove(move)
    
    def getbot(self):
        return self.bot