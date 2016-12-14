"""This program allows human and/or computer players to play the card game BS.
The program uses several different classes: Card, Player, Deck, World, and SetupWidget.
The program starts by creating a World object to keep track of the players, the deck, etc.
Then the program creates a setup window (an object of the class SetupWidget) using Tkinter that allows users to add players.
The values from the setup window are validated (and, if valid, passed in to create a Player object and add it to the world)
every time the ‘add player’ button is pressed. Then, the program allows users to play the game. Each time it is a player’s turn,
the player can see their hand and select their Cards via a Tkinter window. The Cards are then added into the World’s pile.
Once a player has taken their turn, other players are asked if they call BS, and if they do, the program checks to see
if the current player was telling the truth and takes appropriate action, moving the Cards as needed. This continues
until one player has no cards left. Interaction with the user(s) will occur through Tkinter windows (pressing buttons,
checking checkboxes, etc.)."""

# imports
from world import *
from tkinter_for_cards import *

unit_tests = False

def setUpGame(logfile=None):  # fix logfile stuff
    """The code to set up the game"""
    # log = open(logfile, 'w')
    thisWorld = World(logfile=logfile, verbose=True)  # create a World  # change to log
    root = Tk()
    setupwindow = SetupWidget(world=thisWorld, master=root)  # create a setup window to set up the game
    root.mainloop()
    thisWorld.addAllCards()  # add all the cards to the deck
    thisWorld.deal()  # deal the cards to all the players
    thisWorld.createWindow()  # create the window to start the game


# main code
# how to ask for a logfile
logfile = open('test.txt', 'w')  # open the logfile
logfile.write('hi')
setUpGame(logfile=logfile)  # start the game # ERROR logfile not opening
logfile.close()
if unit_tests:
    world = World(logfile='test.txt', verbose=True)
    root = Tk()
    setupwindow = SetupWidget(world=world, master=root)
    root.mainloop()
    world._deck.addAllCards()
    world.deal()
