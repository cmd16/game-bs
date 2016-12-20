"""Catherine DeJager (cmd38)
12/15/2016
CS 106 Final Project: BS
A class to represent the world. The world keeps track of the players, the deck, the current turn number, etc."""

from deck import *
from player import *
import time

class World:
    """A class to represent the world."""
    def __init__(self, deck=None, logfile=None, verbose=False):
        """Create a world object"""
        self.log = logfile
        if deck is None:  # if no Deck is given, create a Deck
            self._deck = Deck()
        else:
            self._deck = deck
        self._playerlist = []  # a list of the world's players
        self._turn_num = 0  # set to 0 because turn_num is incremented at the beginning of each player's turn
        self.verbose = verbose
        self._window = None
        self.start = None
        self.currentplayer = None
        self._text = None
        self._message = None
        self._message_var = None
        self._card_stat = None
        self._card_stat_var = None
        if self.log is not None:
            self.log.write('Created a World object.\n')
        if self.verbose:
            print('Created a World object.')

    def getDeckLen(self):
        """Return the number of cards in the deck"""
        return self._deck.getNumCards()

    def updateMessage(self, message):
        """Change the message displayed in the window"""
        if self.log is not None:
            self.log.write("Updating the message to " + message)
        if self.verbose:
            print("Updating the message to", message)
        self._message_var.set(message)

    def setCurrentPlayer(self, player):
        """Set the current player"""
        if self.log is not None:
            self.log.write("Setting the current player to " + player.name + '\n')
        if self.verbose:
            print("Setting the current player to " + player.name)
        self.currentplayer = player

    def getCurrentPlayer(self):
        """Return the current player"""
        if self.log is not None:
            self.log.write("Returning the current player\n")
        if self.verbose:
            print("Returning the current player")
        return self.currentplayer

    def createWindow(self):
        """Create the window that shows each player's info and displays their buttons"""
        if self.log is not None:
            self.log.write("Creating the world's window\n")
        if self.verbose:
            print("Creating the world's window")
        self._window = Tk()
        self._window.title('Playing BS')
        self.start = Button(self._window, text='start game',
                            command=self.startGame)  # later fix this to include logfile
        self.start.grid(row=0, column=self.getNumPlayers()//2)  # grid the start button in the center on top
        self._message_var = StringVar()
        self._message = Message(self._window, textvariable=self._message_var)
        self._message_var.set("Welcome to the game BS!")
        self._message.grid(row=1, column=self.getNumPlayers())
        self._card_stat_var = StringVar()
        self._card_stat = Message(self._window, textvariable=self._card_stat_var)
        self._card_stat.grid(row=0, column=self.getNumPlayers()+1)
        for idx in range(self.getNumPlayers()):
            self._playerlist[idx].createFrame(self._window, idx)  # tell each player to create their frame
        self._window.mainloop()

    def startGame(self):
        """Start the game"""
        if self.log is not None:
            self.log.write("Starting game\n")
        if self.verbose:
            print("Starting game")
        self.start.grid_forget()
        for player in self.getPlayerList():
            if player.findCard("Ace of Clubs") is not False:
                self.setCurrentPlayer(player)
                print("The player with the Ace of Clubs, %s, goes first." % self.getCurrentPlayer().name)
                break
        else:  # if somehow no player has the Ace of Clubs
            self.setCurrentPlayer(self.getPlayerList()[0])
        for player in self.getPlayerList():  # initialize all the estimates
            if isinstance(player, Cpu):
                player.initialize_estimate()
        self.getCurrentPlayer().takeTurn()

    def incTurnNum(self):
        """Increment the turn number"""
        if self.log is not None:
            self.log.write("Incrementing the turn number\n")
        if self.verbose:
            print("Incrementing the turn number")
        if self._turn_num == 13:
            self._turn_num = 1
        else:
            self._turn_num += 1
        if self.log is not None:
            self.log.write("turn_num is" + str(self._turn_num)+"\n")
        if self.verbose:
            print("turn_num is", self._turn_num)

    def getTurnNum(self):
        """Accessor method to return turn_num"""
        if self.log is not None:
            self.log.write("Returning turn_num\n")
        if self.verbose:
            print("Returning turn_num")
        return self._turn_num

    def addAllCards(self):
        """Add all the cards to the world's deck."""
        if self.verbose:
            print("Adding all the cards to the world's deck")
        if self.log is not None:
            self.log.write("Adding all the cards to the world's deck\n")
        self._deck.addAllCards()

    def giveAllCards(self, player):
        """Give all the deck's cards to the specified player"""
        if self.verbose:
            print("Giving all the cards to " + str(player))
        if self.log is not None:
            self.log.write("Giving all the cards to " + str(player) + '\n')
        self._deck.giveAllCards(player)

    def getPlayerList(self):
        """Accessor method to get the world's list of players"""
        if self.log is not None:
            self.log.write("Returning the world's list of players\n")
        return self._playerlist

    def createPlayer(self, name, verbose=False, difficulty=None, risk=None, pb=None, random=None):
        """Create a Player and add it to the list of players. If given computer values, then create a Cpu."""
        # if None is not in (difficulty, risk, pb, verbose):
        if difficulty is not None:
            if self.log is not None:
                self.log.write("Creating a Cpu object: name %s difficulty %d risk %d pb %s verbose %s\n" % (name, difficulty,
                                                                                                     risk, pb, verbose))
            if self.verbose:
                print("Creating a Cpu object: name %s difficulty %d risk %d pb %s verbose %s" % (name, difficulty,
                                                                                                     risk, pb, verbose))
            self._playerlist.append(Cpu(name, difficulty, risk, pb, verbose, random, world=self, logfile=self.log))
        else:
            if self.log is not None:
                self.log.write('Creating a Player object: name %s verbose %s\n' % (name, verbose))
            if self.verbose:
                print('Creating a Player object: name %s verbose %s' % (name, verbose))
            self._playerlist.append(Player(name, verbose, world=self, logfile=self.log))

    def getPlayerNameStrings(self):  # USED FOR DEBUGGING ONLY
        result = ""
        for item in self._playerlist:
            result += str(item) + ". "
        return result

    def getCpuStrings(self):  # USED FOR DEBUGGING ONLY
        result = []
        for item in self._playerlist:
            if isinstance(item, Cpu):
                result.append(str(item))
            else:
                print("not cpu:", item)
        return result

    def getNumPlayers(self):
        """Get the number of players"""
        if self.log is not None:
            self.log.write('Getting the number of players.\n')
        if self.verbose:
            print("Getting the number of players")
        return len(self._playerlist)

    def deal(self):
        """Deals all the deck's cards to all the players."""
        if self.log is not None:
            self.log.write('Dealing cards to %s\n' % self._playerlist)
        if self.verbose:
            print('Dealing cards to %s' % self._playerlist)
        self._deck.deal(self._playerlist)

    def playCards(self, player, card_seq):
        """Take the cards from the player's hand and put them in the world's deck."""
        if self.log is not None:
            self.log.write('Playing %s from %s into the deck.\n' % (card_seq, player))
        if self.verbose:
            print('Playing %s from %s into the deck.' % (card_seq, player))
        self._deck.addCards(card_seq)
        player.removeCards(card_seq)

    def getNextPlayer(self, player):
        """Get the next player from the list of players"""
        # needs the parameter player because it's not always getting the next player from the current player
        if self.log is not None:
            self.log.write('Getting the next player.\n')
        if self.verbose:
            print('Getting the next player.')
        try:
            index = self._playerlist.index(player)
            if index < self.getNumPlayers() - 1:  # if the player is not the last player in the list
                return self._playerlist[index + 1]
            return self._playerlist[0]
        except ValueError:
            print("Error: player does not exist.")

    def getPreviousPlayer(self, player):
        """Returns the previous player"""
        if self.log is not None:
            self.log.write('Getting the previous player.\n')
        if self.verbose:
            print('Getting the previous player.')
        try:
            index = self._playerlist.index(player)
            if index == 0:  # if the player is the first player in the list
                return self._playerlist[-1]  # return the last player in the list
            return self._playerlist[index - 1]
        except ValueError:
            print("Error: player does not exist.")

    def checkBs(self, prosecutor):
        """Checks whether the accused player was lying or not and moves all the cards in the pile to the appropriate player."""
        if self.verbose:
            print('Calling Bs')
        if self.log is not None:
            self.log.write('Calling Bs')
        defendant = self.getCurrentPlayer()  # defendant is the current player; the one who played the cards earlier
        prosecutor.BSConfig(DISABLED)
        honesty = True  # assume the player told the truth, then change later if needed
        cards = []  # a local list of the cards the player played
        print(defendant.name + " played " + str(defendant.getnumplayed()) + " cards ") # ERROR WITH NUMPLAYED
        for i in range(-1, - defendant.getnumplayed() - 1, -1):
            if self.verbose:
                print('deck is now ' + str(self._deck))
            if self.log is not None:
                self.log.write('deck is now ' + str(self._deck))
            if self.verbose:
                print("adding " + str(self._deck[i]))
            cards.append(self._deck[i])
            if self._deck[i].get_number() != self._turn_num:  # if the number of the card doesn't match the number that should have been played
                honesty = False
        if self.verbose:
            print('cards are ' + str(cards))
        if self.log is not None:
            self.log.write('cards are ' + str(cards))
        self.updateMessage(str(cards))  # show a list of the cards that were played
        print(cards)
        time.sleep(2)
        if self.verbose:
            print('cards:', cards)
        if self.log is not None:
            self.log.write('cards: ' + str(cards))
        if honesty:
            self.giveAllCards(prosecutor)  # take a look at what this is doing
            # these need to move
            self.updateMessage("%s was telling the truth! The cards from the pile have been added to %s's hand." % (
                defendant.name, prosecutor.name))
            # check to see if the hand is empty
            defendant.checkHandLength()
            for player in self.getPlayerList():
                if isinstance(player, Cpu):
                    pass
                    player.add_estimate(prosecutor, [c.get_number() for c in cards])
        else:
            self.giveAllCards(defendant)
            self.updateMessage("%s was lying! The cards from the pile have been added to %s's hand." % (
                defendant.name, defendant.name))
            for player in self.getPlayerList():
                if isinstance(player, Cpu):
                    pass
                    player.add_estimate(defendant, [c.get_number() for c in cards])
        # now it is next player's turn
        print("current player is " + self.getCurrentPlayer().name)
        print("next player is " + self.getNextPlayer(self.getCurrentPlayer()).name)
        self.getNextPlayer(self.getCurrentPlayer()).takeTurn()

    def askBs(self, player):
        """Enable the buttons that allow a player to call (or not call) BS."""
        if self.verbose:
            print('Allowing to %s call BS' % player)
        if self.log is not None:
            self.log.write('Allowing to %s call BS' % player)
        self.getPreviousPlayer(player).BSConfig(DISABLED)  # don't allow that player to call bs anymore this turn
        if player == self.getCurrentPlayer():
            player.checkHandLength()
            self.getNextPlayer(player).takeTurn()  # get the next player and tell them to take a turn
        else:
            player.BSConfig(NORMAL)
            if isinstance(player, Cpu):
                player.calculateBs()
