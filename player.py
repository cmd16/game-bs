"""Catherine DeJager (cmd38)
12/15/2016
CS 106 Final Project: BS
A class to represent players. Each player has a name and a hand of Cards."""

# FIGURE OUT BUG: WITH CPU PLAYERS, SOMETIMES AFTER CHECKING BS, A PLAYER'S TURN IS SKIPPED (AND THE SHOWHAND BUTTON
# IS NOT DISABLED

"""
Documentation for AIs - bluffing:
    Difficulty level
        Play a random card
        Figure out which card they would need to play next and don’t play that, then pick a random card from all the others
        Play whichever card they have the most of that they won’t play next # fix this?
        Play whichever card they will play last
        Play whichever card they will play last that there are the least of in the estimate dictionary
    Risk level
        Always play one card
        Sometimes play two cards
        Sometimes play three cards
        Sometimes play four cards
        Sometimes play one or more bluff cards with real cards
    Random level
        Always follow pattern
        5% chance of choosing a random card
        10% chance of choosing a random card
        15% chance of choosing a random card
        20% chance of choosing a random card
Documentation for AIs - calling BS:
    Difficulty level
        If self has the cards such that the opponent can’t possibly have as many cards as they played, then call bs
        Look at cards moved when bs is called and use that to estimate what each player has
        Look at what each player claims to have played and use that to estimate where cards are
        Look at player bluffing patterns and use that to estimate where cards are
        Look at at player calling bs patterns and use that to estimate where cards are
    Risk level
        If the pile is 2 cards or less then call bs
        If the pile is 4 cards or less than call bs
        If the pile is 6 cards or less then call bs
        If the pile is 8 cards or less then call bs
        If the pile is 10 cards or less then call bs
    Random level
        Always follow pattern
        5% chance of switching choice
        10% chance of switching choice
        15% chance of switching choice
        20% chance of switching choice
"""

from tkinter import *
from global_functions import *
import random

player_tests = False
cpu_tests = False  # look at later

class Player:
    """A class to represent players. Each player has a name and a hand of Cards."""

    def __init__(self, name, verbose=False, world=None, logfile=None):
        """Players start out with a name and an empty hand."""
        self.name = name  # used in print so that the human player can tell who is who
        self.hand = []  # an empty list into which the player's cards will be added
        self.world = world  # keeps track of the world the player belongs to
        self.tkhand = None  # used for tkinter
        self.verbose = verbose
        self.honesty = True  # a boolean that changes every turn depending on whether the player lied or not
        self.numplayed = 0  # an integer that changes every turn depending on how many cards the player played
        self.log = logfile  # a file object
        # these next few variables are used for the tkinter frame to display the cards
        self.frame = None
        self.name_label = None
        self.hand_len_label = None
        self.showhandbutton = None
        self.cardframe = None
        self.bsbutton = None
        self.notbsbutton = None
        self.scrollbar = None
        if self.log is not None:
            self.log.write(self.name + 'created a Player object\n')

    def createFrame(self, window, column):
        """Create a frame for displaying player stats and buttons"""
        self.frame = Frame(window)  # a frame to hold the buttons
        self.frame.grid(column=column, row=1)
        self.name_label = Label(self.frame, text=self.name)  # a label with the player's name
        self.name_label.grid()
        self.hand_len_label = Label(self.frame, text=str(
            self.gethandlength()) + ' cards')  # a label to show the number of cards a player has
        self.hand_len_label.grid(row=2)
        self.bsbutton = Button(self.frame, text='Call BS', command=lambda: self.world.checkBs(self),
                               state=DISABLED)  # a button that allows the player to call Bs
        self.bsbutton.grid(row=3)
        self.notbsbutton = Button(self.frame, text="Don't call BS",
                                  command=lambda: self.world.askBs(self.world.getNextPlayer(self)), state=DISABLED)
        self.notbsbutton.grid(row=4)
        self.showhandbutton = Button(self.frame, text="Show hand", command=self.tkSelectHand, state=DISABLED)
        self.showhandbutton.grid(row=5)

    def updateWindow(self):
        """Updates the label that shows how many cards the player has"""
        if self.verbose:
            print(self.name, "Updating the label that shows the number of cards")
        if self.log is not None:
            self.log.write(self.name + " Updating the label that shows the number of cards\n")
        if self.frame is not None:
            if self.gethandlength() > 0:  # if the player has cards
                self.hand_len_label.config(
                    text=str(self.gethandlength()) + ' cards')  # change the hand length label to the /
                #  number of cards the player has

    def checkHandLength(self):
        """Check to see if there are no cards. If there are no cards, print a congratulatory message and exit the game."""
        if self.gethandlength() == 0:
            print(self.name, "wins!")
            sys.exit(0)

    def getnumplayed(self):
        """Accessor method for the number of cards played"""
        if self.verbose:
            print(self.name, 'Getting the number of cards played')
        if self.log is not None:
            self.log.write(self.name + ' Getting the number of cards played\n')
        return self.numplayed

    def sortHand(self):
        """Sorts the player's hand by numerical order"""
        if self.verbose:
            print(self.name, 'Sorting hand.')
        if self.log is not None:
            self.log.write(self.name + ' Sorting hand\n')
        self.hand.sort(key=lambda x: x.get_number())

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
        # PUTTING IN A TEMPORARY FIX
        for player in self.world.getPlayerList():
            if player.showhandbutton['state'] == NORMAL:
                print('Not ' + self.name + "'s turn yet")
                return
        if self.verbose:
            print(self.name, "Taking a turn")
        if self.log is not None:
            self.log.write(self.name + " Taking a turn")
        self.world.setCurrentPlayer(self)  # tell the world to set it's current player to self
        self.world.incTurnNum()  # update the world's turn number
        self.world.updateMessage(self.name + "'s turn to play " + cardNumToStr(self.world.getTurnNum()) + 's')
        self.tkConfigureShowHand(NORMAL)  # allow the player to click the 'show hand' button

    def BSConfig(self, state):
        """Enables or disables the buttons allowing the user to call BS or not"""
        if self.verbose:
            print(self.name, "Changing the state of the BS buttons to", state)
        if self.log is not None:
            self.log.write(self.name + ' Changing the state of the BS buttons to ' + str(state) + '\n')
        self.bsbutton.config(state=state)
        self.notbsbutton.config(state=state)
        if state == NORMAL:  # if the player's Bs buttons and not bs buttons are enabled
            for player in self.world.getPlayerList():
                if player is not self:
                    player.bsbutton.config(state=DISABLED)  # disable all the other players' bs and not bs buttons

    def tkSelectHand(self):
        """Shows the player's hand and allows the player to select up to 4 cards."""
        self.tkConfigureShowHand(DISABLED)  # disable the button that allows the player to show their cards
        self.cardframe = Frame(self.frame)  # create a frame in which to display the cards
        self.cardframe.grid()
        self.tkhand = [[x, IntVar()] for x in self.hand]  # a list to hold the card objects and the variables to
        # refer to whether the checkbuttons are checked or not
        if self.verbose:
            print(self.name, ' tk hand is ', self.tkhand)
        if self.log is not None:
            self.log.write(self.name + ' tk hand is %s\n' % self.tkhand)
        for idx in range(len(self.tkhand)):
            self.tkhand[idx].append(
                Checkbutton(self.cardframe, text=str(self.tkhand[idx][0]), variable=self.tkhand[idx][1],
                            command=self.checkBoxes))
            # create checkbutton to allow players to select their cards, storing the variables and cards within them
            self.tkhand[idx][2].grid()
        if self.verbose:
            print(self.name, ' tk hand is ', self.tkhand)
        if self.log is not None:
            self.log.write(self.name + ' tk hand is %s\n' % self.tkhand)
        submit = Button(self.cardframe, text="Submit",
                        command=self.playCards)  # create a button to allow the player to submit their cards
        submit.grid()

    def playCards(self, card_seq=None):
        """Play cards into the world's pile. Check if the player lied or not and record that info. Also record how many
        cards were played."""
        self.numplayed = 0  # keep track of how many cards were played this round
        self.honesty = True
        cards_played = []  # a list to keep track of the played cards
        for idx in range(len(self.tkhand)):
            if self.tkhand[idx][1].get() == 1:
                if self.verbose:
                    print(self.name, 'found a selected card:', self.tkhand[idx][0])
                if self.log is not None:
                    self.log.write(self.name + ' found a selected card: %s\n' % self.tkhand[idx][0])
                # put in a method to remove the card from the hand and add it to the deck world's deck. Then change checkBs
                cards_played.append(self.tkhand[idx][0])  # ok so this is what I need to change
                self.hand.remove(self.tkhand[idx][0])  # so this function didn't actually work
                #  so I need to change this
                self.numplayed += 1
                if self.tkhand[idx][0].get_number() != self.world.getTurnNum():
                    if self.verbose:
                        print(self.name, 'found a bluff card:', self.tkhand[idx][0])
                    if self.log is not None:
                        self.log.write(self.name + ' found a bluff card: %s\n' % self.tkhand[idx][0])
                    self.honesty = False
        self.tkConfigureShowHand(DISABLED)  # disable the show hand button
        self.cardframe.destroy()  # destroy the card frame
        if self.numplayed == 0:  # if the player played no cards, make them try again
            print('No cards were played.')
            self.tkSelectHand()
            return
        if self.verbose:
            print(numToWord(self.numplayed))
        if self.log is not None:
            self.log.write(numToWord(self.numplayed))
        self.world.playCards(self, cards_played)  # add the played cards to the world's deck
        summary = self.name + " played " + numToWord(self.numplayed) + " " + cardNumToStr(
            self.world.getTurnNum())  # record how many cards the player played and what number they should be
        if self.numplayed > 1:  # if the player played more than one card, make the number word plural
            summary += "s"
        self.world.updateMessage(summary)
        self.world.askBs(self.world.getNextPlayer(self))  # ask the next player if they call Bs

    def checkBoxes(self):
        """Counts how many checkboxes are checked. Disables other checkboxes is 4 are checked, enables all checkboxes if
        less than 4 are checked."""
        if self.verbose:
            print(self.name, 'A checkbox was checked.')
        if self.log is not None:
            self.log.write(self.name + ' A checkbox was checked.\n')
        numchecked = 0
        for idx in range(len(self.tkhand)):
            if self.tkhand[idx][1].get() == 1:  # if the checkbox is checked
                if self.verbose:
                    print(self.name, 'found a checked box:', self.tkhand[idx][0])
                if self.log is not None:
                    self.log.write(self.name + 'found a checked box:' + str(self.tkhand[idx][0]))
                numchecked += 1
        for idx in range(len(self.tkhand)):
            if numchecked == 4:
                if self.tkhand[idx][1].get() == 0:  # if the checkbox isn't checked
                    self.tkhand[idx][2].config(state=DISABLED)  # disable the checkbox
                    if self.verbose:
                        print(self.name, 'disabled an unchecked checkbox:', self.tkhand[idx][0])
                    if self.log is not None:
                        self.log.write(self.name + ' disabled an unchecked checkbox: %s\n' % self.tkhand[idx][0])
            else:  # enable all the checkboxes
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
            try:
                self.hand.remove(self.findCard(str(item)))
            except ValueError:
                print(item, "error")
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
    def __init__(self, name, difficulty, risk, pb, verbose, random, world=None, logfile=None):
        Player.__init__(self, name, verbose, world, logfile)
        self.difficulty = difficulty  # an integer that represents how hard it is to beat the computer
        # harder players have more/better strategies
        self.risk = risk  # an integer that represents how likely the computer is to accuse another player of lying
        # if a cpu doesn't know for sure that another player is lying,
        # their risk value determines how likely they are to accuse the player
        self.pb = pb  # a boolean value. If this value is set to true, the cpu will tell you when it has succesfully lied
        self.verbose = verbose
        self.world = world
        self.estimate_dict = {}

    def initialize_estimate(self):
        """Initialize the dictionary to hold the estimates of who has what cards"""
        if self.verbose:
            print(self.name + " initializing estimate dictionary")
        if self.log is not None:
            self.log.write(self.name + " initializing estimate dictionary\n")
        for player in self.world.getPlayerList():
            self.estimate_dict[player] = []
        if self.verbose:
            print(self.name + " estimate dictionary is " + str(self.estimate_dict))
        if self.log is not None:
            self.log.write(self.name + " estimate dictionary is " + str(self.estimate_dict) + '\n')

    def add_estimate(self, player, num_seq):
        """Add a number to the player's estimate"""
        if self.verbose:
            print(self.name + " adding " + str(num_seq) + " to " + player.name + "'s estimate")
        if self.log is not None:
            self.log.write(self.name + " adding " + str(num_seq) + " to " + player.name + "'s estimate\n")
        self.estimate_dict[player].extend(num_seq)

    def remove_estimate(self, player, num_seq):
        """Remove a number from the player's estimate"""
        if self.verbose:
            print(self.name + " removing " + str(num_seq) + " from " + player.name + "'s estimate")
        if self.log is not None:
            self.log.write(self.name + " removing " + str(num_seq) + " from " + player.name + "'s estimate\n")
        for num in num_seq:
            self.estimate_dict[player].remove(num)

    def __str__(self):
        return self.name + ', ' + str(len(self.hand)) + ' cards, ' + 'difficulty level: ' + str(self.difficulty) \
               + ', risk level: ' + str(self.risk) + ', pb: ' + str(self.pb) + ', verbose: ' + str(self.verbose)

    def findCardsByNum(self, number):
        """Find all the cards of a given number"""
        if self.verbose:
            print(self.name + " finding all cards of number " + str(number))
        if self.log is not None:
            self.log.write(self.name + " finding all cards of number " + str(number) + "\n")
        result = []
        for card in self.hand:
            if card.get_number() == number:
                result.append(card)
        return result

    def countCardsByNum(self, number):
        """Count the occurrences of cards of a given number"""
        if self.verbose:
            print(self.name + " counting all cards of number " + str(number))
        if self.log is not None:
            self.log.write(self.name + " counting all cards of number " + str(number) + "\n")
        return len(self.findCardsByNum(number))

    def tkSelectHand(self):
        """The method to select cards. Starts out same as regular players, then does calculations."""
        if self.verbose:
            print(self.name, 'selecting hand: ' + str(self.hand))
        if self.log is not None:
            self.log.write(self.name + " selecting hand: " + str(self.hand) + '\n')
        self.tkConfigureShowHand(DISABLED)  # disable the button that allows the player to show their cards
        cards_played = []
        for card in self.hand:
            if card.get_number() == self.world.getTurnNum():  # check to see if there are any honest cards
                cards_played.append(card)
        if cards_played:  # if there are honest cards, then play them # DOES THIS WORK
            if self.verbose:
                print(self.name + " found honest cards: " + str(cards_played))
            if self.log is not None:
                self.log.write(self.name + " found honest cards: " + str(cards_played) + "\n")
            self.playCards(cards_played)
        else:  # bluff
            if self.verbose:
                print(self.name + " bluffing")
            if self.log is not None:
                self.log.write(self.name + " bluffing")
            # num_cards_to_play = random.randint(1, self.risk)  # choose how many cards to play this round
            card_num_list = [x.get_number() for x in self.hand]  # create a list to hold the cards and how many of each card there is
            card_freq_list = []
            for num in range(1, 15):
                count = card_num_list.count(num)
                if 0 < count <= self.risk:
                    card_freq_list.append([num, count])  # append the number of the card and the frequency of that card
            if len(card_freq_list) == 0:  # if there aren't any cards with a low enough frequency, just get all the cards
                for num in range(1, 15):
                    count = card_num_list.count(num)
                    if count > 0:
                        card_freq_list.append([num, count])
            if self.verbose:
                print(self.name + ' card num list: ' + str(card_num_list))
            if self.log is not None:
                self.log.write(self.name + ' card num list: ' + str(card_num_list))
            if self.verbose:
                print(self.name + ' card frequency list: ' + str(card_freq_list))
            if self.log is not None:
                self.log.write(self.name + ' card frequency list: ' + str(card_freq_list))
            if self.difficulty == 1:
                card_minilist = random.choice(card_freq_list)  # pick a random card
                if self.verbose:
                    print(self.name + " random choice of " + str(card_minilist))
                if self.log is not None:
                    self.log.write(self.name + " random choice of " + str(card_minilist))
                # HOLD OFF ON THIS
                cards_played.extend(self.findCardsByNum(card_minilist[0]))  # find all the cards of that number and play them
            elif self.difficulty == 2:
                next_num = (self.world.getTurnNum() + self.world.getNumPlayers()) % 14  # calculate which card would be played next
                if self.verbose:
                    print(self.name + ' would play ' + str(next_num) + ' next.')
                if self.log is not None:
                    self.log.write(self.name + ' would play ' + str(next_num) + ' next.\n')
                if len(card_freq_list) > 1:  # if the length of the list is 1, then you don't want to remove items from it
                    for item in card_freq_list:
                        if item[0] == next_num:
                            if self.verbose:
                                print(self.name + " removing an item that would be played next: " + str(item))
                            if self.log is not None:
                                self.log.write(self.name + " removing an item that would be played next: " + str(item) + "\n")
                            card_freq_list.remove(item)  # get rid of cards that would be played next turn
                    card_minilist = random.choice(card_freq_list)  # pick a random card
                    if self.verbose:
                        print(self.name + " random choice of " + str(card_minilist))
                    if self.log is not None:
                        self.log.write(self.name + " random choice of " + str(card_minilist))
                    # HOLD OFF ON THIS
                    cards_played.extend(self.findCardsByNum(card_minilist[0]))
            elif self.difficulty == 3:
                sys.exit('Cpu difficulty 3 not implemented yet')
                next_num = self.world.getTurnNum() + self.world.getNumPlayers()
                most_num = 0  # the number of the card that the Cpu has the most of
                # FIX THIS
                for j in range(len(self.tkhand)):
                    pass
            if len(cards_played) == 0:
                print("empty list. Trying again")
                self.tkSelectHand()
            if self.verbose:
                print(self.name, "played " + str(cards_played))
            if self.log is not None:
                self.log.write(self.name + " played " + str(cards_played))
            self.playCards(cards_played)

    def playCards(self, card_seq=None):
        """The Cpu way to play cards (cards to play are in a list, not in the tkhand). card_seq=None to match the signature
        of the method in the parent class."""
        if self.verbose:
            print(self.name + " playing " + str(card_seq))
        if self.log is not None:
            self.log.write(self.name + " playing " + str(card_seq))
        self.numplayed = len(card_seq)
        print(self.name + " numplayed is " + str(self.getnumplayed()))  # DEBUG
        self.world.playCards(self, card_seq)
        self.tkConfigureShowHand(DISABLED)
        summary = self.name + " played " + numToWord(self.numplayed) + " " + cardNumToStr(
            self.world.getTurnNum())  # record how many cards the player played and what number they should be
        if self.numplayed > 1:  # if the player played more than one card, make the number word plural
            summary += "s"
        self.world.updateMessage(summary)
        self.world.askBs(self.world.getNextPlayer(self))  # ask the next player if they call Bs

    def calculateBs(self):
        """The Cpu method to guess whether the player was honest or not and choose whether to call bs or not."""
        if self.verbose:
            print(self.name + " calculating probability of bs")
        if self.log is not None:
            self.log.write(self.name + ' calculating probability of bs')
        if self.world.getCurrentPlayer().gethandlength() <= 4:
            self.world.checkBs(self)
        if self.world.getCurrentPlayer().getnumplayed() + self.countCardsByNum(self.world.getTurnNum()) > 4:
            # if the number of cards played and the number of honest cards self has add up to more than 4, then
            # the current player must have been lying
            if self.verbose:
                print(self.name + " knows the player must be lying.")
            if self.log is not None:
                self.log.write(self.name + " knows the player must be lying.")
            self.world.checkBs(self)
            return
        else:
            print(self.name + " can't be certain that the player is lying.")
        if self.risk * 2 >= self.world.getDeckLen():
            if self.difficulty == 2:
                if self.verbose:
                    print("Checking the estimate dictionary: " + str(self.estimate_dict))
                if self.log is not None:
                    self.log.write("Checking the estimate dictionary: " + str(self.estimate_dict))
                if self.world.getTurnNum() not in self.estimate_dict[self.world.getCurrentPlayer()]:
                    if self.verbose:
                        print(self.name + " did not find the given number in the player's estimate dictionary")
                    if self.log is not None:
                        self.log.write(self.name + " did not find the given number in the player's estimate dictionary\n")
                    self.world.checkBs(self)
        self.world.askBs(self.world.getNextPlayer(self))  # MOVE THIS LINE LATER


if player_tests:
    print('this worked')
    p = Player("joe", True, logfile=open('test.txt', 'w'))
    assert p.name == 'joe'
    assert p.verbose
    # name difficulty risk pb verbose random
    player = Cpu('c', 1, 1, False, True, 1)
    root = Tk()
    player.createFrame(root, 1)
    root.mainloop()

if cpu_tests:
    import world
    import card
    this_world = world.World()
    # tests to see what happens when a Cpu knows that the other player must be lying
    this_world.createPlayer('a', True, 1, 1)
    this_world.createPlayer('b', True, 1, 1)
    this_world.createPlayer('c', True, 1, 1)
    this_world.createPlayer('d', True, 1, 1)
    this_world.getPlayerList()[0].addCards(
        [card.Card(1, 2), card.Card(2, 1), card.Card(2, 2), card.Card(2, 3), card.Card(2, 4)])
    this_world.getPlayerList()[1].addCards(
        [card.Card(1, 3), card.Card(3, 1), card.Card(3, 2), card.Card(3, 3), card.Card(3, 4)])
    this_world.getPlayerList()[2].addCards(
        [card.Card(1, 4), card.Card(4, 1), card.Card(4, 2), card.Card(4, 3), card.Card(4, 4)])
    this_world.getPlayerList()[3].addCards(
        [card.Card(1, 1), card.Card(5, 1), card.Card(5, 2), card.Card(5, 3), card.Card(5, 4)])
    this_world.createWindow()
