from tkinter import *
import sys
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


def gameBs(world, logfile=None):
    """The main code to play the game BS"""
    # move into main loop
    for player in world.getPlayerList():
        if player.findCard("Ace of Clubs") is not False:
            world.setCurrentPlayer(player)
            print("The player with the Ace of Clubs, %s, goes first." % world.getCurrentPlayer().name)
            break
    else:  # if somehow no player has the Ace of Clubs
        world.setCurrentPlayer(world.getPlayerList()[0])
        # adding in to deal with new functionality
        world.updateTurnNum(1)
    # changing from the while True loop. If this doesn't work, then revert.
    world.getCurrentPlayer().takeTurn()
    #log.close() # fix later


def askBs(player, world):
    """Enable the buttons that allow a player to call (or not call) BS."""
  # create a variable to keep track of which player to ask and initialize it to the next player after the current player
    # should move into method of world
    '''message = current.name + " played " + numToWord(current.getnumplayed()) + " " + numToStr(turn_num)
    if current.numplayed > 1:  # if the player played more than one card, make the number word plural
        message += "s"'''
    world.getPreviousPlayer(player).BSConfig(DISABLED)  # don't allow that player to call bs anymore this turn
    if player == world.getCurrentPlayer():
        if player.gethandlength() == 0:  # duplicated code: could move into function
            print(player.name, "wins!")  # change .name to getName()
            sys.exit(0)
        world.getNextPlayer(player).takeTurn()
    else:
        player.BSConfig(NORMAL)
    '''for x in range(world.getNumPlayers() - 1):
        """if players[x] == currentPlayer:
            print("skipped")
            continue"""
        message = "%s has %d cards and there are %d cards in the pile. %s, do you call bs?" % (current.name,
                                                current.gethandlength(), len(world.getPile()), this_player.name)
        this_player.BSConfig(NORMAL)
        if y_or_n("%s has %d cards and there are %d cards in the pile. %s, do you call bs?" %
                          (current.name, current.gethandlength(),
                           len(current.pile), this_player.name), False):  # ask the next player if they call bs
            checkBs(current, this_player, turn)  # fix the get next player
            break
        if world.getbs():
            break
        this_player = world.getNextPlayer(this_player)'''

def checkBs(defendant, prosecutor, world):
    """Checks whether the accused player was lying or not and moves all the cards in the pile to the appropriate player."""
    # should move to method of world
    world.calledbs()
    prosecutor.BSConfig(DISABLED)
    if defendant.getHonesty():
        world.emptyPile(prosecutor)
        print("%s was telling the truth! The cards from the pile have been added to %s's hand." % (
            defendant.name, prosecutor.name))
        # check to see if the hand is empty
        if defendant.gethandlength() == 0:
            print(defendant.name, "wins!")  # change .name to getName()
            sys.exit(0)
    else:
        world.emptyPile(defendant)
        print("%s was lying! The cards from the pile have been added to %s's hand." % (defendant.name, defendant.name))
    # now it is next player's turn
    world.getNextPlayer(world.getCurrentPlayer()).takeTurn()
