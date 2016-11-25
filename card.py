import PIL.Image
import PIL.ImageTk
from tkinter import *
class Card:
    """A class to represent playing cards. Card objects should not be changed."""
    def __init__(self, number, suit):
        """Each card has an integer from 1 to 14 representing a number and an integer from 1 to 4 representing a suit. Each card also has a string representation."""
        self._number = number
        self._suit = suit
        #self._suitStr = numToSuit(self._suit)
        #self._numStr = numToStr(self._number)
        '''self._pic = PIL.ImageTk.PhotoImage(
            PIL.Image.open('/Users/cat/PycharmProjects/myCS106/Final_project/PNG-cards-1.3/%s.png' %(str(self).replace(" ","_").lower())))
        self._label = None'''

    def __repr__(self):
        """Overrides an existing object method so that the card value returned is one that can be read by the user.
        __repr__() is used when printing objects in a list, so this ensures that when python prints out a player's hand,
            a human can read the card names."""
        return str(self)

    def __str__(self):
        result = ""
        if self._number == 1:
            result += "Ace"
        elif self._number == 11:
            result += "Jack"
        elif self._number == 12:
            result += "Queen"
        elif self._number == 13:
            result += "King"
        else:  # if the card is a number card, the function converts the number to a string and return the string
            result += str(self._number)
        result += " of "
        if self._suit == 1:
            result += "Hearts"
        elif self._suit == 2:
            result += "Diamonds"
        elif self._suit == 3:
            result += "Spades"
        elif self._suit == 4:
            result += "Clubs"
        return result

    '''def showSelf(self, master):
        self._label = Label(master=master, image=self._pic)
        self._label.pack()'''

'''window = Tk()
c = Card(3, 2)
c.showSelf(window)
window.mainloop()'''