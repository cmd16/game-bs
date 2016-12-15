"""Catherine DeJager (cmd38)
12/15/2016
CS 106 Final Project: BS
A class to represent playing cards."""

from tkinter import *
from global_functions import cardNumToStr

class Card:
    """A class to represent playing cards. Card objects should be immutable."""
    def __init__(self, number, suit):
        """Each card has an integer from 1 to 14 representing a number and an integer from 1 to 4 representing a suit.
        Each card also has a string representation."""
        self._number = number
        self._suit = suit

    def __repr__(self):
        """Overrides an existing object method so that the card value returned is one that can be read by the user.
        __repr__() is used when printing objects in a list, so this ensures that when python prints out a player's hand,
            a human can read the card names."""
        return str(self)

    def get_number(self):
        """accessor method for number"""
        return self._number

    def __lt__(self, other):
        """A function to compare the number value of cards. returns True if self < other."""
        if self._number < other.get_number():
            return True

    def __str__(self):
        result = cardNumToStr(self._number) + " of "
        if self._suit == 1:
            result += "Hearts"
        elif self._suit == 2:
            result += "Diamonds"
        elif self._suit == 3:
            result += "Spades"
        elif self._suit == 4:
            result += "Clubs"
        return result

if '__name__' == '__main__':
    c = Card(3, 2)
    assert c.get_number() == 3
    assert c._suit == 2
