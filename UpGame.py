import itertools
import random

class Game:

    suits = ['c', 'd', 'h', 's']
    values = ['A', 'K', 'Q', 'J', '10', '8', '7', '6', '5', '4', '3', '2']
    deck = set(itertools.product(values, suits))
    nextRound = False

    state = {
        "players" : [],
        "pot" : 0,
        "rounds" : ["show", "pre", "flop", "turn", "river", "showdown"],
        "round" : 0,
        "cards" : [],
        "dealt" : [],
        "actionOn" : 0,
        "currBet" : 0
    }

    def newPlayer(self, player):
        self.state['players'] = self.state['players'] + [player]

    def deal(self):
        for player in self.state['players']:
            newCards = []
            for i in range(0,4):
                newCards.append(self.state['cards'].pop(len(self.state['cards'])-1))
            player.deal(newCards)

    def readyDeck(self):
        self.state['cards'] = random.sample(self.deck,(5 + 4 * len(self.state['players'])))

    def actionMoves(self):
        self.state['actionOn'] = (self.state['actionOn'] + 1) % len(self.state['players'])
        currentPlayer = self.state['players'][self.state['actionOn']]
        while(currentPlayer.status == 'folded'):
            self.state['actionOn'] = (self.state['actionOn'] + 1) % len(self.state['players'])
            currentPlayer = self.state['players'][self.state['actionOn']]
        if(self.state['round'] == 0):
            print("showing")
            if(len(currentPlayer.upcards) != 0):
                self.nextRound = True
                self.state['round'] += 1
                self.state['actionOn'] = -1
        else:
            print("not showing")
            if(currentPlayer.currBet == self.state['currBet'] and currentPlayer.status != "none"):
                self.nextRound = True
                self.state['round'] += 1
                self.state['actionOn'] = -1

    def applyMove(self, player, move):
        if (move[0] == "show"):
            self.state['players'][player].show(move[1])
        elif (move[0] == "check"):
            self.state['players'][player].check()
        elif (move[0] == "fold"):
            self.state['players'][player].fold()
        elif (move[0] == "bet"):
            self.state['players'][player].bet(move[1])
            self.state['currBet'] = self.state['players'][player].currBet
            self.state['pot'] += move[1]

    def newRound(self):
        for player in self.state['players']:
            if(player.status != "folded"):
                player.currBet = 0
                player.status = "none"
        self.state['currBet'] = 0
        self.state['actionOn'] = 0
        self.nextRound = False

    def dealFlop(self):
        dealtCards = []
        for i in range(0,3):
            dealtCards.append(self.state['cards'].pop(len(self.state['cards'])-1))
        self.state['dealt'].append(dealtCards)

    def dealTurn(self):
        self.state['dealt'].append(self.state['cards'].pop(len(self.state['cards'])-1))

    def dealRiver(self):
        self.state['dealt'].append(self.state['cards'].pop(len(self.state['cards'])-1))

    def showdown(self):
        for player in self.state['players']:
            if(player.status != "folded"):
                player.upcards.append(player.downcards)
                player.downcards = []

class Player:
    chips = 0
    position = 0
    upcards = []
    downcards = []
    status = "none"
    currBet = 0

    def deal(self, cards):
        self.downcards = cards

    def fold(self):
        self.status = 'folded'
        self.currBet = 0

    def check(self):
        self.status = 'check'

    def bet(self, amount):
        self.chips -= amount
        self.status = 'bet'
        self.currBet += amount

    def show(self, cards):
        self.upcards = cards
        for c in cards:
            self.downcards.remove(c)
        print(self.upcards)


if __name__=='__main__':
    game = Game()
    game.newPlayer(Player())
    game.newPlayer(Player())
    game.newPlayer(Player())
    game.readyDeck()
    game.deal()
    game.printGame()
