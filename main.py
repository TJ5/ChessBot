
import berserk 
from game import Game
import threading
F = open('lichess.token', 'r')
token = F.readline()

session = berserk.TokenSession(token)
client = berserk.Client(session)
print(client.account.get_email()) #test client is working

fendict = {}
for event in client.bots.stream_incoming_events():
    
    #logic to filter out variants 
    if event['type'] == 'challenge':
        print(event)
        if event['challenge']['variant']['key'] == "standard" or event['challenge']['variant']['key'] == "fromPosition":
            if (event['challenge']['speed'] == "correspondence"):
                if (event['challenge']['variant']['key'] == "fromPosition"):
                    fendict[event['challenge']['id']] = event['challenge']['initialFen']
                else:
                    fendict[event['challenge']['id']] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                client.bots.accept_challenge(event['challenge']['id'])
            else:
                client.bots.decline_challenge(event['challenge']['id'])
        else: 
            client.bots.decline_challenge(event['challenge']['id'])
    elif event['type'] == 'gameStart':
        print(event)
        #Call a Game object that handles the stream of state changes of the game 
        id = event['game']['id']
        try:
            fen = fendict[event['game']['id']]
            game = Game(client, id, fen)
        except: 
            
            game = Game(client, id)
        
        game.start()    

        
