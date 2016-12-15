"""Catherine DeJager (cmd38)
12/15/2016
CS 106 Final Project: BS
A widget to set up the game by getting user input (names, computer player options, etc.) and then creating Player
    objects using the given input as parameters."""

from tkinter import *
from player import *
from world import *
from deck import *

class SetupWidget:
    """A widget to set up the game by getting user input (names, computer player options, etc.) and then creating Player
    objects using the given input as parameters."""
    def __init__(self, world=None, master=None):
        self._window = master
        self._window.title("Setup")
        self._world = world
        self._playername = StringVar()
        self._playerentry = Entry(self._window, textvariable=self._playername)
        self._playerentry.pack()
        self._cpuvar = IntVar()
        self._cpuoption = Checkbutton(self._window, variable=self._cpuvar, text='Computer player?', command=self.toggleCpuOptions)
        self._playername.set("Enter name here")
        self._addplayerbutton = Button(self._window, text="Add player", command=self.createPlayer)
        self._addplayerbutton.pack(side=BOTTOM)
        self._invalidlabel = Label(self._window)
        self._validlabel = Label(self._window)
        self._difficultyvar = IntVar()
        self._difficultyslider = Scale(self._window, variable=self._difficultyvar, label='Difficulty level:',
                                       orient=HORIZONTAL, from_=1, to=5, sliderlength=15)
        self._riskvar = IntVar()
        self._riskslider = Scale(self._window, variable=self._riskvar, label='Risk level:',
                                 orient=HORIZONTAL, from_=1, to=5, sliderlength=15)
        self._pbvar = BooleanVar()
        self._pbcheckbox = Checkbutton(self._window, variable=self._pbvar, text='Do you want the computer to tell you when it has successfully lied?')
        self._verbosevar = BooleanVar()
        self._verbosecheckbox = Checkbutton(self._window, variable=self._verbosevar, text='Turn on verbose output?')
        self._verbosecheckbox.pack()
        self._cpuoption.pack()

    def createPlayer(self):  # first need to check that all inputs are valid
        """Checks that the user has entered valid input. If the input is invalid, show an error message.
        If the input is valid, create a player with the given input and add it to self's world's list of players."""
        self._invalidlabel.pack_forget()
        self._validlabel.pack_forget()
        if not self._playername.get().isalpha():  # check to see if the name is alphanumeric characters
            self._invalidlabel['text'] = "Invalid input: please use only letters with no spaces."
            self._invalidlabel.pack()
            return
        for item in self._world.getPlayerList():
            if self._playername.get() == item.name:
                self._invalidlabel['text'] = "Invalid input: another player already has the name %s." % item.name
                self._invalidlabel.pack()
                return
        self._addplayerbutton['state'] = NORMAL
        self._validlabel.config(text='Player added: ' + self._playername.get())
        self._validlabel.pack()
        if self._cpuvar.get() == 1:
            self._world.createPlayer(self._playername.get(), self._riskvar.get(), self._pbvar.get(), self._verbosevar.get())
        else:
            self._world.createPlayer(self._playername.get(), self._verbosevar.get())

    def toggleCpuOptions(self):
        """If the cpu checkbox is checked, show the cpu options. If the cpu checkbox is unchecked, hide the cpu options."""
        if self._cpuvar.get() == 1:
            self._difficultyslider.pack()
            self._riskslider.pack()
            self._pbcheckbox.pack()
        else:
            self._difficultyslider.pack_forget()
            self._riskslider.pack_forget()
            self._pbcheckbox.pack_forget()

    def printcpuvalues(self):
        """Prints the values of the input for the cpu options. This method used for debugging only."""
        print('difficulty:', self._difficultyvar.get(), 'risk:', self._riskvar.get(), 'pb:', self._pbvar.get(),
              'verbose:', self._verbosevar.get())


if "__name__" == "__main__":
    this_world = World()
    this_world._playerlist.append(Player("Joe"))
    root = Tk()
    myApp = SetupWidget(world=this_world, master=root)
    root.mainloop()
    print(myApp._world.getPlayerNameStrings())
    for item in this_world._playerlist:
        print(type(item))
    print(myApp._world.getCpuStrings())
    myApp.printcpuvalues()
#else:
    this_world = World()
    root = Tk()
    myApp = SetupWidget(world=this_world, master=root)
    root.mainloop()
