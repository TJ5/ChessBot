import chess as c 
import berserk 


F = open('lichess.token', 'r')
token = F.readline()

session = berserk.TokenSession(token)
client = berserk.Client(session)
print(client.account.get_email()) #test client is working