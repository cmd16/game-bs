"""Catherine DeJager (cmd38)
12/15/2016
CS 106 Final Project: BS
A class to represent players. Each player has a name and a hand of Cards."""

"""
Documentation for AIs - bluffing:
    Difficulty level
        Play a random card
        Figure out which card they would need to play next and don’t play that, then pick a random card from all the others
        Play whichever card they have the most of that they won’t play next # fix this?
        Play whichever card they will play last
        Play whichever card they will play last that they have the most of # fix this?
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
"""

from tkinter import *
from global_functions import *
import random

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

    def __str__(self):
        return self.name + ', ' + str(len(self.hand)) + ' cards, ' + 'difficulty level: ' + str(self.difficulty) \
               + ', risk level: ' + str(self.risk) + ', pb: ' + str(self.pb) + ', verbose: ' + str(self.verbose)

    def findCardsByNum(self, number):
        """Find all the cards of a given number"""
        if self.verbose:
            print("Finding all cards of number " + str(number))
        if self.log is not None:
            self.log.write("Finding all cards of number " + str(number))
        result = []
        for card in self.hand:
            if card.get_number() == number:
                result.append(card)
        return result

    def tkSelectHand(self):
        """The method to select cards. Starts out same as regular players, then does calculations."""
        if self.verbose:
            print(self.name, 'selecting hand')
        if self.log is not None:
            self.log.write(self.name + " selecting hand")
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
            if card_freq_list is None:  # if there aren't any cards with a low enough frequency, just get all the cards
                for num in range(1, 15):
                    count = card_num_list.count(num)
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
                    print(self.name + " random choice of " + card_minilist)
                if self.log is not None:
                    self.log.write(self.name + " random choice of " + card_minilist)
                # HOLD OFF ON THIS
                cards_played.extend(self.findCardsByNum(card_minilist[0]))  # find all the cards of that number and play them
            elif self.difficulty == 2:
                sys.exit('Cpu difficulty 2 not implemented yet')
                next_num = self.world.getTurnNum() + self.world.getNumPlayers()  # calculate which card would be played next
                # FIX THIS
                while True:
                    check = self.tkhand[random.randint(len(self.tkhand))]
                    if check[0].get_number() != next_num:
                        break
                check[1] = 1  # check the checkbox
            elif self.difficulty == 3:
                sys.exit('Cpu difficulty 3 not implemented yet')
                next_num = self.world.getTurnNum() + self.world.getNumPlayers()
                most_num = 0  # the number of the card that the Cpu has the most of
                # FIX THIS
                for j in range(len(self.tkhand)):
                    pass
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
        self.world.playCards(self, card_seq)
        print(numToWord(self.numplayed))
        print(cardNumToStr(self.world.getTurnNum()))
        summary = self.name + " played " + numToWord(self.numplayed) + " " + cardNumToStr(
            self.world.getTurnNum())  # record how many cards the player played and what number they should be
        if self.numplayed > 1:  # if the player played more than one card, make the number word plural
            summary += "s"
        self.world.updateMessage(summary)
        self.world.askBs(self.world.getNextPlayer(self))  # ask the next player if they call Bs


if __name__ == "__main__":
    print('this worked')
    p = Player("joe", True, logfile=open('test.txt', 'w'))
    assert p.name == 'joe'
    assert p.verbose
    # name difficulty risk pb verbose random
    player = Cpu('c', 1, 1, False, True, 1)
    root = Tk()
    player.createFrame(root, 1)
    root.mainloop()
