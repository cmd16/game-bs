"""
This program allows human and/or computer players to play the card game BS"""
# STUFF TO FIX: Get from playing cards to asking BS, Create a stats window. Get PIL working to show cards. Create AIs.
# Limit the number of players that can be created
# Look at changing pile to deck object
# override membership in Player so that if card in self returns True if the card is in the player's hand

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
debugsetup = False


def setUpGame(logfile=None):  # fix logfile stuff
    """The code to set up the game"""
    if debugsetup:
        print('setting up game')
    # log = open(logfile, 'w')
    thisWorld = World(logfile=logfile, verbose=True)  # change to log
    root = Tk()
    setupwindow = SetupWidget(world=thisWorld, master=root)
    root.mainloop()
    thisWorld._deck.addAllCards()
    thisWorld.deal()
    thisWorld.createWindow()


# main code
# how to ask for a logfile
logfile = open('test.txt', 'w')
logfile.write('hi')
setUpGame(logfile=logfile)  # ERROR
# gameBs(logfile='test.txt')
logfile.close()
if unit_tests:
    world = World(logfile='test.txt', verbose=True)
    root = Tk()
    setupwindow = SetupWidget(world=world, master=root)
    root.mainloop()
    world._deck.addAllCards()
    world.deal()
