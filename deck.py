from random import shuffle
from player import *
from card import *


class Deck:
    """A class to model a deck of cards."""
    def __init__(self):
        """Creates a deck object."""
        self._cards = []

    def __getitem__(self, key):
        """A method to access cards by index"""
        return self._cards[key]

    def addAllCards(self):
        """Creates one card of each suit for each number/face and adds it to the deck."""
        for i in range(1, 14):
            for j in range(1, 5):
                c = Card(i, j)
                self._cards.append(c)

    def shuffle_cards(self):
        """Shuffles the deck."""
        shuffle(self._cards)

    def giveCards(self, player, num):
        """Adds the specified number of cards to the player's hand and removes those cards from the deck."""
        player.addCards(self._cards[:num])
        self._cards = self._cards[num:]

    def giveAllCards(self, player):
        """Adds all the cards to the player's hand and removes those cards from the deck"""
        player.addCards(self._cards[:])
        self._cards = []

    def deal(self, playerList):
        """Given a sequence of players, shuffle the deck and give the same number of cards to each player."""
        if len(playerList) == 0:
            sys.exit("Error: there are no players.")
        self.shuffle_cards()
        handSize = 52 // len(playerList)  # integer division so that if there are extra cards they are not used
        for player in playerList:
            self.giveCards(player, handSize)
            player.sortHand()

    def getCards(self):
        """returns the list of cards in this deck"""
        return self._cards

    def __str__(self):
        """return a string representation of a Deck"""
        return str([str(x) for x in self._cards])

    def removeTopCard(self):
        """Remove the top card and return it"""
        # assumption: top card is index -1 and bottom card is index 0
        return self._cards.pop()

    def returnTopCard(self):
        """Return the top card without removing it from the deck."""
        return self._cards[-1]

    def addCards(self, card_seq):
        """card_seq is a sequence (a list or tuple) of Card objects.  Add them to the end of the _cards list."""
        self._cards.extend(card_seq)

    def getNumCards(self):
        """returns the number of cards in the deck"""
        return len(self._cards)