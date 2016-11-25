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
        self.log = logfile
        self.frame = None
        self.label = None
        self.handnumlabel = None

    def createFrame(self, window, column):
        """Create a frame for displaying player stats"""
        self.frame = Frame(window)
        self.frame.grid(column=column)
        self.label = Label(self.frame,text=self.name)
        self.label.grid()
        self.handnumlabel = Label(self.frame, text=self.gethandlength())
        self.handnumlabel.grid()

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

    def showHand(self):
        """Opens a window which shows the player their hand (Ace of clubs, 5 of Spades, etc.)"""
        root = Tk()
        msg = Message(root, text=self.hand)
        msg.config(bg='white', font=('times', 24))
        msg.pack()
        root.mainloop()

    def sortHand(self):
        """Sorts the player's hand by numerical order"""
        if self.verbose:
            print(self.name, 'Sorting hand.')
        self.hand.sort(key=lambda x: x._number)

    def gethandlength(self):
        """Gets the length of the player's hand."""
        if self.verbose:
            print(self.name, "Checking the length of hand.")
        if self.log is not None:
            self.log.write(self.name + " Checking the length of hand.\n")
        return len(self.hand)

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
        next = Button(root, text="Show hand", command=lambda: self.tkSelectHand(turn_num, root))
        next.pack()  # later implement pack_forget()
        root.mainloop()

    def tkSelectHand(self, turn_num, root):
        """Shows the player's hand and allows the player to select up to 4 cards."""
        self.tkhand = [[x, IntVar()] for x in self.hand]
        if self.verbose:
            print(self.name, ' tk hand is ', self.tkhand)
        if self.log is not None:
            self.log.write(self.name + ' tk hand is %s\n' % self.tkhand)
        for idx in range(len(self.tkhand)):
            self.tkhand[idx].append(Checkbutton(root, text=str(self.tkhand[idx][0]), variable=self.tkhand[idx][1],
                                                command=self.checkHand))
            self.tkhand[idx][2].pack()
        submit = Button(root, text="Submit", command=lambda: self.playCards(turn_num, root))
        submit.pack()

    def playCards(self, turn_num, root):
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
                if self.tkhand[idx][0]._number != turn_num:
                    if self.verbose:
                        print(self.name, 'found a bluff card.')
                    if self.log is not None:
                        self.log.write(self.name + ' found a bluff card.\n')
                    self.honesty = False
        self.numplayed = numplayed
        # self.tkhand = []
        root.destroy()

    def checkHand(self):
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

    def selectHand(self, turnNum):  # turnNum is the number (4, 11, etc.) the player must play this turn
        """Given a player and the number that the player must player this turn, allow the player to play 1 to 4 cards and record whether the player lied or not"""
        if self.verbose:
            print(self.name, 'Selecting hand.')
        played = []
        self.pile = []
        if type(turnNum) is int:
            turnCard = numToStr(turnNum)
        else:
            print("Error. The value for the turn number is not an integer.")
            return None
        """for j in range(numPlayed):  # for each card the player wants to select, a new window is opened;
                                        # the player chooses one card at a time
            root = Tk()
            v = IntVar()
            # creates a label telling the player which number they must play this round
            Label(root, text="Your turn to play " + roundCard, justify=LEFT, padx=20).pack()
            for i in range(1,14):
                # counts how many cards with the current value are in the hand by creating a list and finding its length
                numCount = len([x for x in self.hand if x.number == i])
                if numCount > 0:  # if the player has at least one card of the current value
                    txt = numToStr(i) + ": " + str(numCount)
                    Radiobutton(root, text = txt, variable=v, value= i).pack(anchor=W)
            mainloop()"""
            # Button(root, text = "Submit", command = submit)
        input(self.name + ", you need to play %ss. Press 'Enter' to see your hand and continue." %turnCard).strip()
        print('Your hand:', self.hand)
        numPlayed = input("How many cards do you want to play? Enter a number from 1 to 4: ").strip()
        # move into a function validatecard()
        if self.verbose:
            print(self.name, 'Validating card')  # why does this happen before the numPlayed line?
        try:
            numPlayed = int(numPlayed)
        except ValueError:
            print("Invalid input. Number of cards to play set to default, 1.")
            correct_input = False
            numPlayed = 1
        if not 1 <= numPlayed <= 4:
            print("Invalid input. Number of cards to play set to default, 1.")
            correct_input = False
            numPlayed = 1
        if numPlayed > len(self.hand):
            print("You don't have that many cards. Number of cards to play set to default, 1.")
        for i in range(numPlayed):
            cardPlay = input("What card do you want to play? -->").strip()
            while True:  # wait this looks wrong
                if self.findCard(nameToCardName(cardPlay)) is not False:
                    break
                cardPlay = input("You don't have that card. Try again. What card do you want to play? -->").strip()
            cardPlayed = self.findCard(nameToCardName(cardPlay))
            if cardPlayed._number == int(turnNum):
                honest = True
            else:
                honest = False
            if self.verbose:
                print(self.name, 'Honesty is', honest)
                print(self.name, 'Card played is', cardPlayed)
            self.pile.append([cardPlayed, turnCard, honest])
            if self.verbose:
                print(self.name, 'Pile is', self.pile)
            # debugging
            print(self.findCard(cardPlayed))
            self.hand.remove(self.findCard(cardPlayed))  # why isn't find card working
            print('Your hand:', self.hand)
        print("\n" * 12)  # prints blank lines so the next player doesn't see what was actually played
        # prints how many cards the player played and their alleged value
        message = self.name + " played " + numToWord(numPlayed) + " " + turnCard
        if numPlayed > 1:  # if the player played more than one card, make the number word plural
            message = message + "s"
        print(message)
        # self.pile.extend(played)  # why does extend work and append doesn't?
        if self.verbose:
            print(self.name, 'Pile is now', self.pile)

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

    def findCardIdx(self, name):
        """finds the index of a specific card, e.g, Ace of Spades"""
        if self.verbose:
            print(self.name, 'Searching hand for index of', name)
        try:
            return self.hand.index(name)
        except ValueError:
            print("Error, %s not in hand." % name)

class Cpu(Player):  # a cpu is still a player, so it inherits from the Player class, but because it's not human, it works differently
    # __init__ overrides the parent class because the cpu needs some attributes that human players don't need
    def __init__(self, name, difficulty, risk, pb, verbose, world=None):
        super(Cpu, self).__init__(self)
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