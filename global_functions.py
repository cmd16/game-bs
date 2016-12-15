"""Catherine DeJager (cmd38)
12/15/2016
CS 106 Final Project: BS
A module to model a deck of cards.
Functions used by multiple files in the project."""

def cardNumToStr(n):
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
