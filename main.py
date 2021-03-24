
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
        print(event)
        if event['challenge']['variant']['key'] == "standard":
            #if event['challenge']['challenger']['id'] == 'yeastape':
            client.bots.accept_challenge(event['challenge']['id'])
            #else:
            #   client.bots.decline_challenge(event['challenge']['id'])
            #Logic for when to accept/deny here
        else: 
            client.bots.decline_challenge(event['challenge']['id'])
    elif event['type'] == 'gameStart':
        pass
        #Call a Game object that handles the stream of state changes of the game 
        id = event['game']['id'] 
        game = Game(client, id)
        game.start()    

        
