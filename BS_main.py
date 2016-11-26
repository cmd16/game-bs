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
from global_functions import *

# global variables
debug = False
debug2 = False
debug3 = False
unit_tests = False
debug4 = False

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
    thisWorld.createWindow()
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
            currentPlayer.tkConfigureShowHand(NORMAL)
            askBs(currentPlayer, turn_num, thisWorld)
            if currentPlayer.gethandlength() == 0:
                print(currentPlayer.name, "wins!")
                sys.exit(0)
            currentPlayer.tkConfigureShowHand(DISABLED)
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