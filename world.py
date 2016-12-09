from deck import *
from player import *
# from BS_main import gameBs MOVED TO LATER IN THE FILE TO AVOID CIRCULAR IMPORTS

class World:
    """A class to represent the world."""
    def __init__(self, deck=None, logfile=None, verbose=False):
        """Create a world object"""
        self.log = logfile
        if deck == None:  # if no Deck is given, create a Deck
            self._deck = Deck()
        else:
            self._deck = deck
        self._playerlist = []  # a list of the world's players
        self._bscalled = False  # this is basically just a global variable
        self._pile = []
        self._turn_num = 1
        self.verbose = verbose
        if self.log is not None:
            self.log.write('Created a World object.\n')
        if self.verbose:
            print('Created a World object.')
        self._window = None
        self.start = None
        self.currentplayer = None
        self._text = None

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
        return self.currentplayer

    def createWindow(self):
        """Create the window that shows each player's info and displays their buttons"""
        if self.log is not None:
            self.log.write("Creating the world's window\n")
        if self.verbose:
            print("Creating the world's window")
        self._window = Tk()
        self._window.title('Playing BS')
        #from BS_main import gameBs
        self.start = Button(self._window, text='start game',
                            command=self.startGame)  # later fix this to include logfile
        self.start.grid(row=0, column=len(self._playerlist)//2)  # grid the start button in the center on top
        for idx in range(len(self._playerlist)):
            self._playerlist[idx].createFrame(self._window, idx)  # tell each player to create their frame
        self._text = Text(self._window)
        self._text.insert(INSERT, 'hi')  # from tutorialspoint. Error takes up a bunch of space
        '''self._text.grid(row=0, column=len(self._playerlist))  # the column is at the end of the list of players'''
        self._window.mainloop()

    def startGame(self):
        """Start the game by playing"""
        if self.log is not None:
            self.log.write("Starting game\n")
        if self.verbose:
            print("Starting game")
        self.start.grid_forget()
        from global_functions import gameBs
        gameBs(self)

    def updateTurnNum(self, turn_num):
        """Update the turn number"""
        if self.log is not None:
            self.log.write("Updating turn number\n")
        if self.verbose:
            print("Updating turn number")
        self._turn_num = turn_num

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

    def getTurnNum(self):
        """Accessor method to return turn_num"""
        if self.log is not None:
            self.log.write("Returning turn_num\n")
        if self.verbose:
            print("Returning turn_num")
        return self._turn_num

    def getPile(self):
        """Accessor method to return the pile"""
        if self.log is not None:
            self.log.write('Returning the pile.\n')
        if self.verbose:
            print('Returning the pile.')
        return self._pile

    def emptyPile(self, player):
        """Takes all the cards from the pile and gives them to the player"""
        if self.log is not None:
            self.log.write('Emptying the pile and giving all the cards to ' + player.name + '\n')
        if self.verbose:
            print('Emptying the pile and giving all the cards to ' + player.name)
        player.addCards(self.getPile())
        self._pile = []

    def calledbs(self):
        """Mutator method to tell the world that bs was called"""
        if self.log is not None:
            self.log.write('Telling the world that bs was called.\n')
        if self.verbose:
            print('Telling the world that bs was called.')
        self._bscalled = True

    def resetbs(self):  # NOT USED
        """Mutator method to reset bs to False. Called at the beginning of every round."""
        if self.log is not None:
            self.log.write('Resetting the world\'s bs value.\n')
        if self.verbose:
            print('Resetting the world\'s bs value.')
        self._bscalled = False

    def getbs(self):  # NOT USED
        """Accessor method to return tell if bs is called"""
        if self.log is not None:
            self.log.write('Asking the world if bs was called.\n')
        return self._bscalled

    def getPlayerList(self):
        """Accessor method to get the world's list of players"""
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
            self._playerlist.append(Cpu(name, difficulty, risk, pb, verbose, world=self, logfile=self.log))
        else:
            if self.log is not None:
                self.log.write('Creating a Player object: name %s verbose %s\n' % (name, verbose))
            self._playerlist.append(Player(name, verbose, world=self, logfile=self.log))

    def getPlayerNameStrings(self):  # NOT USED
        result = ""
        for item in self._playerlist:
            result += str(item) + ". "
        return result

    def getCpuStrings(self):  # NOT USED
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
            if index < len(self._playerlist) - 1:  # if the player is not the last player in the list
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
        # world.calledbs() removed because not needed NOT USED
        defendant = self.getCurrentPlayer()  # defendant is the current player; the one who played the cards earlier
        if self.verbose:
            print('pile:', self._pile)
        if self.log is not None:
            self.log.write('Checking to see if Bs was called')
        prosecutor.BSConfig(DISABLED)
        if defendant.getHonesty():
            self.emptyPile(prosecutor)  # take a look at what this is doing
            # these need to move
            print("%s was telling the truth! The cards from the pile have been added to %s's hand." % (
                defendant.name, prosecutor.name))
            # check to see if the hand is empty
            if defendant.gethandlength() == 0:
                print(defendant.name, "wins!")  # change .name to getName()
                sys.exit(0)
        else:
            self.emptyPile(defendant)
            print("%s was lying! The cards from the pile have been added to %s's hand." % (defendant.name, defendant.name))
        if self.verbose:
            print('now pile is', self._pile)
        if self.log is not None:
            self.log.write("Now pile is %s\n" % self._pile)
        # now it is next player's turn
        self.getNextPlayer(self.getCurrentPlayer()).takeTurn()

    def askBs(self, player):
        """Enable the buttons that allow a player to call (or not call) BS."""
        # create a variable to keep track of which player to ask and initialize it to the next player after the current player
        # should move into method of world
        '''message = current.name + " played " + numToWord(current.getnumplayed()) + " " + numToStr(turn_num)
        if current.numplayed > 1:  # if the player played more than one card, make the number word plural
            message += "s"'''
        if self.verbose:
            print('Allowing to %s call BS' % player)
        if self.log is not None:
            self.log.write('Allowing to %s call BS' % player)
        self.getPreviousPlayer(player).BSConfig(DISABLED)  # don't allow that player to call bs anymore this turn
        if player == self.getCurrentPlayer():
            if player.gethandlength() == 0:  # duplicated code: could move into function
                print(player.name, "wins!")  # change .name to getName()
                sys.exit(0)
            self.getNextPlayer(player).takeTurn()  # get the next player and tell them to take a turn
        else:
            player.BSConfig(NORMAL)
