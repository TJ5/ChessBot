
import berserk 
from game import Game

F = open('lichess.token', 'r')
token = F.readline()

session = berserk.TokenSession(token)
client = berserk.Client(session)
print(client.account.get_email()) #test client is working

for event in client.bots.stream_incoming_events():
    
    #logic to filter out variants 
    if event['type'] == 'challenge':
        if True:
            client.bots.accept_challenge(event['challenge']['id'])
        elif False:
            pass    
        #Logic for when to accept/deny here
    elif event['type'] == 'gameStart':
        pass
        #Call a Game object that handles the stream of state changes of the game 
        id = event['game']['id']
        game = Game(False, client, id)
        game.start()    
    
        
