"""Catherine DeJager
This program allows human and/or computer players to play the card game BS"""
# STUFF TO FIX: Why do windows pop up weird? Create a stats window. Get PIL working to show cards. Create AIs.

# Note: accessor methods for other programmers to access, in this context ok to access directly
# Look into python properties
# redundant try except is as efficient as it can be, try putting into a function
# try creating a function validateCard

# imports
from world import *
from deck import *
from player import *
from tkinter_for_cards import *

# global variables
debug = False
debug2 = False
debug3 = False
unit_tests = False
debug4 = False

# functions
def y_or_n (msg, default):
    """a function that asks a yes or no question and returns true if yes, false if no, and the default value if neither yes nor no"""
    answer = input(msg).strip()[0].lower()  # this only looks at the first letter and makes it lowercase
    if answer == "y":  # note: "yes","Yeah","yo", etc. all count - all that matters is that the first letter is y
        return True
    elif answer == "n":
        return False
    else:
        print("Invalid input. Value set to ", default)
        return default

def numToStr(n):
    """takes the number value of a card and returns a string."""
    # If the card is a face card, the function returns the string of the corresponding face name
    if n == 1:
        return "Ace"
    elif n == 11:
        return "Jack"
    elif n == 12:
        return "Queen"
    elif n == 13:
        return "King"
    else:  # if the card is a number card, the function converts the number to a string and return the string
        return str(n)

def numToWord(n):
    """Change a number to a word"""
    if n == 1:
        return "one"
    elif n == 2:
        return "two"
    elif n == 3:
        return "three"
    elif n == 4:
        return "four"
    elif n == 5:
        return "five"
    elif n == 6:
        return "six"
    elif n == 7:
        return "seven"
    elif n == 8:
        return "eight"
    elif n == 9:
        return "nine"
    elif n == 10:
        return "ten"


def nameToCardName(name):
    """Gets the full card name given a user input."""
    if "of" in name:  # if the name is in "[card] of [suit]" format
        nameSplit = name.split(" of ")
        fullName = nameSplit[0].capitalize() + " of " + nameSplit[1].capitalize()
        return fullName
    else:  # the name can also be in shorthand (e.g., "3s" for "3 of Spades") format
        try:  # this works only if name starts with a number in a string (e.g. "2")
            if len(name) == 3:
                nameNum = str(int(name[0:2]))  # ATTENTION why did I convert this to a string?
            else:
                nameNum = str(int(name[0]))
        except ValueError:  # this statement is executed if the first character in the string (or first two characters, if length is 3) is not a number
            if name[0].lower() == "a":
                nameNum = "Ace"
            elif name[0].lower() == "j":
                nameNum = "Jack"
            elif name[0].lower() == "q":
                nameNum = "Queen"
            elif name[0].lower() == "k":
                nameNum = "King"
            else:
                print("Error: invalid number value.")
                return -1
        if name[-1].lower() == "h":
            nameSuit = "Hearts"
        elif name[-1].lower() == "d":
            nameSuit = "Diamonds"
        elif name[-1].lower() == "s":
            nameSuit = "Spades"
        elif name[-1].lower() == "c":
            nameSuit = "Clubs"
        else:
            print("Error: invalid suit value.")
            return -1
        return nameNum + " of " + nameSuit

def findCardNum(number, player):
    """finds the index of a card of a given number in a given list"""
    for idx in range(player.gethandlength()):  # a return statement exits the function, which means this function only finds the first card of the given number in the list
        if array[n]._number == number:
            return n
        return False


def findPlayCard(number, player, deck):
    """used for finding the first card of a given value and playing it"""
    x = findCardNum(number, player.hand)  # find the index of the card (i.e., what spot in the list of the player's hand is it found at)
    deck.append(player[x])  # adds the card to the deck
    del player.hand[x]  # removes the card from the player's hand

def checkBs(defendant, prosecutor, world, root):
    """Checks whether the accused player was lying or not and moves all the cards in the pile to the appropriate player."""
    world.calledbs()
    if defendant.getHonesty():
        world.emptyPile(prosecutor)
        print("%s was telling the truth! The cards from the pile have been added to %s's hand." % (
        defendant.name, prosecutor.name))
    else:
        world.emptyPile(defendant)
        print("%s was lying! The cards from the pile have been added to %s's hand." % (defendant.name, defendant.name))
    root.destroy()

def askBs(current, turn_num, world):
    """Loop through the array of players and ask each player if they call BS. If a player says yes, call the checkBS function."""
    this_player = world.getNextPlayer(current)  # create a variable to keep track of which player to ask and initialize it to the next player after the current player
    if debug3:
        print(current.name)
        print(numToWord(current.numplayed))
        print(numToStr(turn_num))
    message = current.name + " played " + numToWord(current.numplayed) + " " + numToStr(turn_num)
    if current.numplayed > 1:  # if the player played more than one card, make the number word plural
        message += "s"
    for x in range(world.getNumPlayers() - 1):
        """if players[x] == currentPlayer:
            print("skipped")
            continue"""
        message = "%s has %d cards and there are %d cards in the pile. %s, do you call bs?" % (current.name,
                                                current.gethandlength(), len(world.getPile()), this_player.name)
        root = Tk()
        # figure out how to close the window, issue where you have to press yes
        ask = Confirm(master=root, message=message, ycommand=lambda: checkBs(current, this_player, world, root),
                      ncommand=root.destroy)
        root.mainloop()
        '''if y_or_n("%s has %d cards and there are %d cards in the pile. %s, do you call bs?" %
                          (current.name, current.gethandlength(),
                           len(current.pile), this_player.name), False):  # ask the next player if they call bs
            checkBs(current, this_player, turn)  # fix the get next player
            break'''
        if world.getbs():
            break
        this_player = world.getNextPlayer(this_player)

def gameBs(logfile=None):
    """The main code to play the game BS"""
    log = open(logfile, 'w')
    thisWorld = World(logfile=log)
    root = Tk()
    setupwindow = SetupWidget(world=thisWorld, master=root)
    root.mainloop()
    thisWorld._deck.addAllCards()
    thisWorld.deal()
    if debug4:
        print('dealt')
    for player in thisWorld.getPlayerList():
        if player.findCard("Ace of Clubs") is not False:
            currentPlayer = player
            print("The player with the Ace of Clubs, %s, goes first." % currentPlayer.name)
            break
    else:  # if somehow no player has the Ace of Clubs
        currentPlayer = thisWorld.getPlayerList()[0]
    while True:
        for turn_num in range(1, 14):
            thisWorld.updateTurnNum(turn_num)
            thisWorld.resetbs()
            currentPlayer.tkShowHand(turn_num)
            askBs(currentPlayer, turn_num, thisWorld)
            if currentPlayer.gethandlength() == 0:
                print(currentPlayer.name, "wins!")
                sys.exit(0)
            currentPlayer = thisWorld.getNextPlayer(currentPlayer)
    log.close()

# main code
gameBs(logfile='test.txt')
if unit_tests:
    thisWorld = World()
    root = Tk()
    setupwindow = SetupWidget(world=thisWorld, master=root)
    root.mainloop()
    thisWorld._deck.addAllCards()
    thisWorld.deal()
    thisWorld.getPlayerList()[0].tkSelectHand(2)