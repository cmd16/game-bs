# game-bs
An implementation in Python of the card game BS (also called Cheat or I Doubt It)
Catherine DeJager (cmd38)
12/15/2016
CS Final Project: BS
This program allows human and/or computer players to play the card game BS.
The program uses several different classes: Card, Player, Deck, World, and SetupWidget.
The program starts by creating a World object to keep track of the players, the deck, etc.
Then the program creates a setup window (an object of the class SetupWidget) using Tkinter that allows users to add players.
The values from the setup window are validated (and, if valid, passed in to create a Player object and add it to the world)
every time the ‘add player’ button is pressed. Then, the program allows users to play the game. Each time it is a player’s turn,
the player can see their hand and select their Cards via a Tkinter window. The Cards are then added into the World’s pile.
Once a player has taken their turn, other players are asked if they call BS, and if they do, the program checks to see
if the current player was telling the truth and takes appropriate action, moving the Cards as needed. This continues
until one player has no cards left. Interaction with the user(s) will occur through Tkinter windows (pressing buttons,
checking checkboxes, etc.).

How to run the game:
    Make sure you have all the files: BS_main.py, deck.py, global_functions.py, player.py, card.py, tkinter_for_cards.py, and world.py
    Make sure you have all the libraries installed: tkinter, random, and time
    Run BS_main.py