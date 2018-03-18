import socket
import itertools
import random
from pickle import dumps, loads
from UpGame import *

HOST, PORT = "localhost", 9998
BUFFSIZE = 1024                 # for socket.send & recv commands
BACKLOG = 2
MIN_PLAYERS = 2

suits = ['c', 'd', 'h', 's']
values = ['A', 'K', 'Q', 'J', '10', '8', '7', '6', '5', '4', '3', '2']
deck = set(itertools.product(suits, values))
clients = []

game = Game()

def distributeState():
    for client in clients:
        client.send(dumps(game.state))

def showdown():
    game.showdown()
    distributeState()

def river():
    game.dealRiver()
    distributeState()
    print("dealt river")
    while(game.nextRound == False):
        playerMove = loads(clients[game.state['actionOn']].recv(BUFFSIZE))
        game.applyMove(game.state['actionOn'], playerMove)
        game.actionMoves()
        distributeState()
    game.newRound()
    print("river complete")

def turn():
    game.dealTurn()
    distributeState()
    print("dealt turn")
    while(game.nextRound == False):
        playerMove = loads(clients[game.state['actionOn']].recv(BUFFSIZE))
        game.applyMove(game.state['actionOn'], playerMove)
        game.actionMoves()
        distributeState()
    game.newRound()
    print("turn complete")

def flop():
    game.dealFlop()
    distributeState()
    print("dealt flop")
    while(game.nextRound == False):
        playerMove = loads(clients[game.state['actionOn']].recv(BUFFSIZE))
        game.applyMove(game.state['actionOn'], playerMove)
        game.actionMoves()
        distributeState()
    game.newRound()
    print("flop complete")

def preflop():
    distributeState()
    while(game.nextRound == False):
        playerMove = loads(clients[game.state['actionOn']].recv(BUFFSIZE))
        game.applyMove(game.state['actionOn'], playerMove)
        game.actionMoves()
        distributeState()
    game.newRound()
    print("betting complete")

def show():
    while(game.nextRound == False):
        playerMove = loads(clients[game.state['actionOn']].recv(BUFFSIZE))
        print(playerMove)
        game.applyMove(game.state['actionOn'],playerMove)
        game.actionMoves()
        distributeState()
    game.newRound()
    print("showing complete")

def playGame():
    game.readyDeck()
    game.deal()
    distributeState()
    show()
    preflop()
    flop()
    turn()
    river()
    showdown()


def start():
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))

    sock.listen(BACKLOG)
    serverip, serverport = sock.getsockname()
    print("Running at %s, %s" % (serverip, serverport))
    #Wait for all players to have joined
    while(len(clients) != MIN_PLAYERS):
        #Receive new client connection
        client, address = sock.accept()
        clientip, clientport = address
        #Maintain list of currently connected clients
        clients.append(client)

        response = ""
        # while True:
        #     try:
        response = client.recv(BUFFSIZE)
        #Client wants to join the game
        if(response in "yY"):
            game.newPlayer(Player())
            print(len(game.state['players']))
            playerId = len(clients)-1
            client.send(dumps(playerId))
    playGame()
    # while True:
    #     distributeState()
    #     game.state = loads(clients[game.state['actionOn']].recv(BUFFSIZE))
    #     game.actionMoves()
            # except EOFError:                            # if available
            #     print("error")
            #     break

if __name__=='__main__':
    start()
