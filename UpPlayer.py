import socket
from pickle import dumps, loads
from UpGame import *

HOST, PORT = "localhost", 9998
BUFFSIZE = 1024                 # for socket.send & recv commands
BACKLOG = 2
playerId = -1
state = {}

def printGame(state):
    print("=======================")
    print("Pot: " + str(state['pot']))
    print("Cards: " + str(state['dealt']))
    print("=======================")
    for i in range(0,len(state['players'])):
        player = state['players'][i]
        print("")
        if(i == playerId):
            print("Player " + str(i) + " " + str(player.downcards) + " || "  + str(player.upcards) + " " + str(player.status) + " " + str(player.currBet))
        else:
            print("Player " + str(i) + ": X X "  + " || " + str(player.upcards) + " " + str(player.status) + " " + str(player.currBet))
        print("")
        print("=======================")
    print("Action on Player %i" % state['actionOn'])
    diff = state['currBet'] - state['players'][state['actionOn']].currBet
    if(diff != 0):
        print("Bet is %i, %i to call" % (state['currBet'], diff))
    print("=======================")

def start():
    global playerId
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    action = input('Join game? ')
    sock.send(action)
    playerId = loads(sock.recv(BUFFSIZE))
    print("id: " + str(playerId))
    while True:
        try:
            state = loads(sock.recv(BUFFSIZE))
            printGame(state)
            move = []
            if(state['actionOn'] == playerId):
                if(state['round'] == 0):
                    cardsToShow = input("Select cards to show: ")
                    move = ["show", cardsToShow]
                else:
                    action = input('Your move: ')
                    if(action == 'fold'):
                        move = ["fold", 0]
                    elif (action == 'bet'):
                        amount = int(input("Enter amount: "))
                        move = ["bet", amount]
                    elif (action == 'check'):
                        move = ["check", 0]
                sock.send(dumps(move))
        except EOFError:
            break

if __name__=='__main__':
    start()
