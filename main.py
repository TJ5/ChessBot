
import berserk 
from game import Game
import threading
F = open('lichess.token', 'r')
token = F.readline()

session = berserk.TokenSession(token)
client = berserk.Client(session)
print(client.account.get_email()) #test client is working
client.challenges.create_ai(level=8, color='white')
#client.challenges.create('yeastApe', False, color = 'black')
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
        if event['game']['id'] in fendict:
            fen = fendict[event['game']['id']]
            game = Game(client, id, fen)
        else:
            
            game = Game(client, id, '8/8/3k4/8/8/4K3/8/4Q3 w - - 0 1')
        
        #game.start()    

        
