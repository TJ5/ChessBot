
import berserk 
from game import Game
import threading
F = open('lichess.token', 'r')
token = F.readline()

session = berserk.TokenSession(token)
client = berserk.Client(session)
print(client.account.get_email()) #test client is working


for event in client.bots.stream_incoming_events():
    
    #logic to filter out variants 
    if event['type'] == 'challenge':
        
        if event['challenge']['variant']['key'] == "standard" and event['challenge']['speed'] == "correspondence":
            client.bots.accept_challenge(event['challenge']['id'])
            print(event)
        else: 
            client.bots.decline_challenge(event['challenge']['id'])
    elif event['type'] == 'gameStart':
        pass
        #Call a Game object that handles the stream of state changes of the game 
        id = event['game']['id'] 
        game = Game(client, id)
        game.start()    

        
