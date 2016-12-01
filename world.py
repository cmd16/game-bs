from deck import *
from player import *
# from BS_main import gameBs MOVED TO LATER IN THE FILE TO AVOID CIRCULAR IMPORTS

class World:
    """A class to represent the world."""
    def __init__(self, deck=None, logfile=open('test.txt', 'w')):
        """Create a world object"""
        self.log = logfile
        if deck == None:  # if no Deck is given, create a Deck
            self._deck = Deck()
        self._playerlist = []
        self._bscalled = False  # this is basically just a global variable
        self._pile = []
        self._turn_num = 1
        if self.log is not None:
            self.log.write('Created a World object.\n')
        self._window = None
        self.start = None
        self.currentplayer = None

    def setCurrentPlayer(self, player):
        """Set the current player"""
        if self.log is not None:
            self.log.write("Setting the current player to " + player.name + '\n')
        self.currentplayer = player

    def getCurrentPlayer(self):
        """Return the current player"""
        if self.log is not None:
            self.log.write("Returning the current player\n")
        return self.currentplayer

    def createWindow(self):
        if self.log is not None:
            self.log.write("Creating the world's window\n")
        self._window = Tk()
        self._window.title('Playing BS')
        #from BS_main import gameBs
        self.start = Button(self._window, text='start game',
                            command=self.startGame)  # later fix this to include logfile
        self.start.grid(row=0, column=1)
        for idx in range(len(self._playerlist)):
            self._playerlist[idx].createFrame(self._window, idx)
        self._window.mainloop()

    def startGame(self):
        if self.log is not None:
            self.log.write("Starting game\n")
        self.start.grid_forget()
        from global_functions import gameBs
        gameBs(self, logfile=self.log)

    def updateTurnNum(self, turn_num):
        """Update the turn number"""
        if self.log is not None:
            self.log.write("Updating turn number\n")
        self._turn_num = turn_num

    def incTurnNum(self):
        """Increment the turn number"""
        if self._turn_num == 13:
            self._turn_num = 1
        else:
            self._turn_num += 1

    def getTurnNum(self):
        """Accessor method to return turn_num"""
        if self.log is not None:
            self.log.write("Returning turn_num\n")
        return self._turn_num

    def getPile(self):
        """Accessor method to return the pile"""
        if self.log is not None:
            self.log.write('Returning the pile.\n')
        return self._pile

    def emptyPile(self, player):
        """Takes all the cards from the pile and gives them to the player"""
        self.log.write('Emptying the pile and giving all the cards to ' + player.name + '\n')
        player.addCards(self.getPile())
        self._pile = []

    def calledbs(self):
        """Mutator method to tell the world that bs was called"""
        if self.log is not None:
            self.log.write('Telling the world that bs was called.\n')
        self._bscalled = True

    def resetbs(self):
        """Mutator method to reset bs to False. Called at the beginning of every round."""
        if self.log is not None:
            self.log.write('Resetting the world\'s bs value.\n')
        self._bscalled = False

    def getbs(self):
        """Accessor method to return tell if bs is called"""
        if self.log is not None:
            self.log.write('Asking the world if bs was called.\n')
        return self._bscalled

    def getPlayerList(self):
        """Accessor method to get the list of players"""
        if self.log is not None:
            self.log.write("Returning the world's list of players\n")
        return self._playerlist

    def createPlayer(self, name, verbose=False, difficulty=None, risk=None, pb=None):
        """Create a Player and add it to the list of players. If given computer values, then create a Cpu."""
        # if None is not in (difficulty, risk, pb, verbose):
        if difficulty is not None:
            if self.log is not None:
                self.log.write("Creating a Cpu object: name %s difficulty %d risk %d pb %s verbose %s\n" % (name, difficulty,
                                                                                                     risk, pb, verbose))
            self._playerlist.append(Cpu(name, difficulty, risk, pb, verbose, world=self))
        else:
            if self.log is not None:
                self.log.write('Creating a Player object: name %s verbose %s\n' % (name, verbose))
            self._playerlist.append(Player(name, verbose, world=self, logfile=self.log))

    def getPlayerNameStrings(self):
        result = ""
        for item in self._playerlist:
            result += str(item) + ". "
        return result

    def getCpuStrings(self):
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
        return len(self._playerlist)

    def deal(self):
        """Deals all the deck's cards to all the players."""
        if self.log is not None:
            self.log.write('Dealing cards to %s\n' % self._playerlist)
        self._deck.deal(self._playerlist)

    def playCards(self, player, card_seq):
        """Take the cards from the player's hand and put them in the world's deck."""
        if self.log is not None:
            self.log.write('Playing %s from %s into the deck.\n' % (card_seq, player))
        self._deck.addCards(card_seq)
        player.removeCards(card_seq)

    def getNextPlayer(self, player):
        """Get the next player from the list of players"""
        # needs the parameter player because it's not always getting the next player from the current player
        if self.log is not None:
            self.log.write('Getting the next player.\n')
        try:
            index = self._playerlist.index(player)
            if index < len(self._playerlist) - 1:  # if the player is not the last player in the list
                return self._playerlist[index + 1]
            return self._playerlist[0]
        except ValueError:
            print("Error: player does not exist.")

    def getPreviousPlayer(self, player):
        if self.log is not None:
            self.log.write('Getting the previous player.\n')
        try:
            index = self._playerlist.index(player)
            if index == 0:  # if the player is the first player in the list
                return self._playerlist[-1]
            return self._playerlist[index - 1]
        except ValueError:
            print("Error: player does not exist.")