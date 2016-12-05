# stuff to fix: get from asking Bs to next turn
from tkinter import *
from global_functions import *

debug = False
class Player:
    """A class to represent players. Each player has a name and a hand."""
    def __init__(self, name, verbose=False, world=None, logfile=None):
        """Players start out with a name and an empty hand."""
        self.name = name  # used in print so that the human player can tell who is who
        self.hand = []  # an empty list into which the player's cards will be added
        self.world = world  # keeps track of the world the player belongs to
        self.tkhand = None  # used for tk
        self.verbose = verbose
        self.honesty = True  # a boolean that changes every turn depending on whether the player lied or not
        self.numplayed = 0  # an integer that changes every turn depending on how many cards the player played
        try:
            self.log = open(logfile, 'w')
        except TypeError:
            print("No logfile was given")
            self.log = None
        self.frame = None
        self.name_label = None
        self.hand_len_label = None
        self.showhandbutton = None
        self.cardframe = None
        self.bsbutton = None
        self.notbsbutton = None
        if self.log is not None:
            self.log.write(str(self) + ' created a Player object\n')

    def createFrame(self, window, column):
        """Create a frame for displaying player stats"""
        self.frame = Frame(window)
        self.frame.grid(column=column, row=1)
        self.name_label = Label(self.frame, text=self.name)
        self.name_label.grid()
        self.hand_len_label = Label(self.frame, text=str(self.gethandlength()) + ' cards')
        self.hand_len_label.grid(row=2)  # changing checkBs so that it gets current player
        self.bsbutton = Button(self.frame, text='Call BS', command=lambda: self.world.checkBs(self), state=DISABLED)
        self.bsbutton.grid(row=3)
        self.notbsbutton = Button(self.frame, text="Don't call BS", command=lambda: askBs(self.world.getNextPlayer(self),
                                                                                          self.world), state=DISABLED)
        self.notbsbutton.grid(row=4)
        self.showhandbutton = Button(self.frame, text="Show hand", command=lambda: self.tkSelectHand(), state=DISABLED)
        self.showhandbutton.grid(row=5)

    def updateWindow(self):
        """Updates the label that shows how many cards the player has"""
        if self.verbose:
            print(self.name, "Updating the label that shows the number of cards")
        if self.log is not None:
            self.log.write(self.name + " Updating the label that shows the number of cards\n")
        if self.frame is not None:
            if self.gethandlength() > 0:
                self.hand_len_label.config(text=str(self.gethandlength()) + ' cards')

    def getnumplayed(self):
        """Accessor method for the number of cards played"""
        if self.verbose:
            print(self.name, 'Getting the number of cards played')
        if self.log is not None:
            self.log.write(self.name + ' Getting the number of cards played\n')
        return self.numplayed

    def getHonesty(self):
        """Accessor method to return if the player lied"""
        return self.honesty

    def sortHand(self):
        """Sorts the player's hand by numerical order"""
        if self.verbose:
            print(self.name, 'Sorting hand.')
        if self.log is not None:
            self.log.write(self.name + ' Sorting hand\n')
        self.hand.sort(key=lambda x: x._number)

    def gethandlength(self):
        """Gets the length of the player's hand."""
        if self.verbose:
            print(self.name, "Checking the length of hand.")
        if self.log is not None:
            self.log.write(self.name + " Checking the length of hand.\n")
        return len(self.hand)

    def tkConfigureShowHand(self, state):
        """Enables or disables the player's 'show hand' button"""
        if self.verbose:
            print(self.name, "Changing the state of the 'show hand' button to", state)
        if self.log is not None:
            self.log.write(self.name + " Changing the state of the 'show hand' button to " + str(state) + '\n')
        self.showhandbutton.config(state=state)

    def takeTurn(self):
        """Gets player ready to take a turn"""
        if self.verbose:
            print(self.name, "Taking a turn")
        if self.log is not None:
            self.log.write(self.name + " Taking a turn")
        self.world.setCurrentPlayer(self)
        self.world.incTurnNum()
        self.world.resetbs()
        self.tkConfigureShowHand(NORMAL)  # may change this later

    def BSConfig(self, state):
        """Enables or disables the buttons allowing the user to call BS or not"""
        if self.verbose:
            print(self.name, "Changing the state of the BS buttons to", state)
        if self.log is not None:
            self.log.write(self.name + ' Changing the state of the BS buttons to ' + str(state) + '\n')
        self.bsbutton.config(state=state)
        self.notbsbutton.config(state=state)
        if state == NORMAL:
            for player in self.world.getPlayerList():
                if player is not self:
                    player.bsbutton.config(state=DISABLED)

    """THIS METHOD NOT USED"""
    def tkShowHand(self, turn_num):
        """Creates a window, tells the player what they need to play and waits for them to click a button to show their hand."""
        if self.verbose:
            print(self.name, 'tk asking to show hand.')
        if self.log is not None:
            self.log.write(self.name + ' tk asking to show hand hand.\n')
        root = Tk()
        root.title('Selecting cards.')
        label = Label(root, text=self.name + ", you need to play %ss." % numToStr(turn_num))
        label.pack()
        next = Button(root, text="Show hand", command=lambda: self.tkSelectHand())
        next.pack()  # later implement pack_forget()
        root.mainloop()

    def tkSelectHand(self):
        """Shows the player's hand and allows the player to select up to 4 cards."""
        self.cardframe = Frame(self.frame)
        self.cardframe.grid()
        self.tkhand = [[x, IntVar()] for x in self.hand]
        if self.verbose:
            print(self.name, ' tk hand is ', self.tkhand)
        if self.log is not None:
            self.log.write(self.name + ' tk hand is %s\n' % self.tkhand)
        for idx in range(len(self.tkhand)):
            self.tkhand[idx].append(Checkbutton(self.cardframe, text=str(self.tkhand[idx][0]), variable=self.tkhand[idx][1],
                                                command=self.checkBoxes))
            self.tkhand[idx][2].grid()
        submit = Button(self.cardframe, text="Submit", command=self.playCards)
        submit.grid()

    def playCards(self):
        """Play cards into the world's pile. Check if the player lied or not and record that info. Also record how many
        cards were played."""
        numplayed = 0
        self.honesty = True
        for idx in range(len(self.tkhand)):
            if self.tkhand[idx][1].get() == 1:
                if self.verbose:
                    print(self.name, 'found a selected card:', self.tkhand[idx][0])
                if self.log is not None:
                    self.log.write(self.name + ' found a selected card: %s\n' % self.tkhand[idx][0])
                self.world._pile.append(self.tkhand[idx][0])
                self.hand.remove(self.tkhand[idx][0])
                numplayed += 1
                if self.tkhand[idx][0]._number != self.world.getTurnNum():
                    if self.verbose:
                        print(self.name, 'found a bluff card:', self.tkhand[idx][0])
                    if self.log is not None:
                        self.log.write(self.name + ' found a bluff card: %s\n' % self.tkhand[idx][0])
                    self.honesty = False
        self.numplayed = numplayed
        self.tkConfigureShowHand(DISABLED)
        self.cardframe.destroy()
        self.updateWindow()
        message = self.name + " played " + numToWord(self.getnumplayed()) + " " + numToStr(self.world.getTurnNum())  # move this into log?
        if self.numplayed > 1:  # if the player played more than one card, make the number word plural
            message += "s"
        print(message)
        askBs(self.world.getNextPlayer(self), self.world)

    def checkBoxes(self):
        """Counts how many checkboxes are checked. Disables other checkboxes is 4 are checked, enables all checkboxes if
        less than 4 are checked."""
        if self.verbose:
            print(self.name, 'A checkbox was checked.')
        if self.log is not None:
            self.log.write(self.name + ' A checkbox was checked.\n')
        numchecked = 0
        for idx in range(len(self.tkhand)):
            if debug:
                print(self.name, 'self.tkhand[%d] is' %idx, self.tkhand[idx])
            if self.tkhand[idx][1].get() == 1:
                if self.verbose:
                    print(self.name, 'found a checked box:', self.tkhand[idx][0])
                numchecked += 1
        for idx in range(len(self.tkhand)):
            if numchecked == 4:
                if self.tkhand[idx][1].get() == 0:
                    self.tkhand[idx][2].config(state=DISABLED)
                    if self.verbose:
                        print(self.name, 'disabled an unchecked checkbox:', self.tkhand[idx][0])
                    if self.log is not None:
                        self.log.write(self.name + ' disabled an unchecked checkbox: %s\n' % self.tkhand[idx][0])
            else:
                self.tkhand[idx][2].config(state=NORMAL)
                if self.verbose:
                    print(self.name, 'enabled a checkbox:', self.tkhand[idx][0])
                if self.log is not None:
                    self.log.write(self.name + ' enabled a checkbox: %s\n' % self.tkhand[idx][0])

    def __str__(self):
        """String representation of player is the player name and number of cards"""
        return self.name + ', ' + str(len(self.hand)) + ' cards'

    def addCards(self, cardSeq):
        """Adds the given cards to the player's hand."""
        if self.verbose:
            print(self.name, 'Adding', cardSeq, 'to hand.')
        if self.log is not None:
            self.log.write(self.name + ' adding %s to hand\n' % cardSeq)
        self.hand.extend(cardSeq)
        self.sortHand()
        if self.verbose:
            print(self.name, 'Hand is now', self.hand)
        if self.log is not None:
            self.log.write(self.name + ' Hand is now %s\n' % self.hand)
        self.updateWindow()

    def removeCards(self, cardSeq):
        """Removes the given cards from the player's hand"""
        if self.verbose:
            print(self.name, 'Removing', cardSeq, 'from hand.')
        if self.log is not None:
            self.log.write(self.name + ' removing %s from hand.\n' % cardSeq)
        for item in cardSeq:
            self.hand.remove(self.findCard(item))
        if self.verbose:
            print(self.name, 'Hand is now', self.hand)
        if self.log is not None:
            self.log.write(self.name + ' hand is now %s\n' % self.hand)
        self.updateWindow()

    def findCard(self, name):
        """Searches the player's hand for the card of a given name. If the card is found, return the card."""
        if self.verbose:
            print(self.name, 'Searching hand for', name)
        if self.log is not None:
            self.log.write(self.name + ' searching hand for %s.\n' % name)
        for item in self.hand:
            if str(item) == name:
                if self.verbose:
                    print(self.name, 'Found', name)
                if self.log is not None:
                    self.log.write(self.name + ' Found %s\n' % name)
                return item
        if self.verbose:
            print(self.name, "Didn't find", name)
        if self.log is not None:
            self.log.write(self.name + " Didn't find %s\n" % name)
        return False

class Cpu(Player):  # a cpu is still a player, so it inherits from the Player class, but because it's not human, it works differently
    # __init__ overrides the parent class because the cpu needs some attributes that human players don't need
    def __init__(self, name, difficulty, risk, pb, verbose, world=None, logfile=None):
        Player.__init__(self, name, verbose, world, logfile)
        self.name = name
        self.hand = []
        self.difficulty = difficulty  # an integer that represents how hard it is to beat the computer
                                    # harder players have more/better strategies
        self.risk = risk  # an integer that represents how likely the computer is to accuse another player of lying
                        # if a cpu doesn't know for sure that another player is lying,
                            # their risk value determines how likely they are to accuse the player
        self.pb = pb  # a boolean value. If this value is set to true, the cpu will tell you when it has succesfully lied
        self.verbose = verbose
        self.world = world

    def __str__(self):
        return self.name + ', ' + str(len(self.hand)) + ' cards, ' + 'difficulty level: ' + str(self.difficulty) \
               + ', risk level: ' + str(self.risk) + ', pb: ' + str(self.pb) + ', verbose: ' + str(self.verbose)

if __name__ == "__main__":
    print('this worked')
    p = Player("joe", True, logfile='test.txt')
    assert p.name == 'joe'
    assert p.verbose