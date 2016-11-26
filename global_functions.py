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


def gameBs(world,logfile=None):
    """The main code to play the game BS"""
    for player in world.getPlayerList():
        if player.findCard("Ace of Clubs") is not False:
            currentPlayer = player
            print("The player with the Ace of Clubs, %s, goes first." % currentPlayer.name)
            break
    else:  # if somehow no player has the Ace of Clubs
        currentPlayer = world.getPlayerList()[0]
    while True:
        for turn_num in range(1, 14):
            world.updateTurnNum(turn_num)
            world.resetbs()
            currentPlayer.tkConfigureShowHand(NORMAL)
            askBs(currentPlayer, turn_num, world)
            if currentPlayer.gethandlength() == 0:
                print(currentPlayer.name, "wins!")
                sys.exit(0)
            currentPlayer.tkConfigureShowHand(DISABLED)
            currentPlayer = world.getNextPlayer(currentPlayer)
    #log.close() # fix later