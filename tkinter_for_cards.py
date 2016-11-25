from tkinter import *
from player import *
from world import *
from deck import *

unit_tests = False
unit2 = False

class Confirm:
    """A class to ask players whether they call BS."""
    def __init__(self, master=None, message=None, ycommand=None, ncommand=None):
        self._window = master
        self._message = message
        self._ycommand = ycommand
        self._ncommand = ncommand
        self._window.title("Calling BS")  # Set title
        # Create a label
        label = Label(self._window, text=message)
        # Create a button
        self._y_n_value = BooleanVar()
        y = Button(self._window, text="Yes", command=self._ycommand)
        n = Button(self._window, text="No", command=self._ncommand)
        # Put the widgets on the window
        label.pack()
        y.pack()
        n.pack()

    def yes(self):
        print("Yes")
        self._window.destroy()
        return True

    def no(self):
        print("No")
        self._window.destroy()
        return False


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
        self._cpuentry = IntVar()
        self._cpuoption = Checkbutton(self._window, variable=self._cpuentry, text='Computer player?', command=self.toggleCpuOptions)
        self._playername.set("Enter name here")
        self._addplayerbutton = Button(self._window, text="Add player", command=self.createPlayer) #later disable
        self._addplayerbutton.pack(side=BOTTOM)
        self._invalidlabel = Label(self._window)
        self._validlabel = Label(self._window, text="Player added.")
        self._difficultyentry = IntVar()
        self._difficultyslider = Scale(self._window, variable=self._difficultyentry, label='Difficulty level:',
                                       orient=HORIZONTAL, from_=1, to=5, sliderlength=15)
        self._riskentry = IntVar()
        self._riskslider = Scale(self._window, variable=self._riskentry, label='Risk level:',
                                       orient=HORIZONTAL, from_=1, to=5, sliderlength=15)
        self._pbentry = BooleanVar()
        self._pbcheckbox = Checkbutton(self._window, variable=self._pbentry, text='Do you want the computer to tell you when it has successfully lied?')
        self._verboseentry = BooleanVar()
        self._verbosecheckbox = Checkbutton(self._window, variable=self._verboseentry, text='Turn on verbose output?')
        self._verbosecheckbox.pack()
        self._cpuoption.pack()

    def createPlayer(self): # first need to check that all inputs are valid
        """Checks that the user has entered valid input. If the input is invalid, show an error message.
        If the input is valid, create a player with the given input and add it to self's world's list of players."""
        self._invalidlabel.pack_forget()
        self._validlabel.pack_forget()
        if not self._playername.get().isalpha():
            self._invalidlabel['text'] = "Invalid input: please use only letters with no spaces."
            self._invalidlabel.pack()
            return
        for item in self._world._playerlist:
            if self._playername.get() == item.name:
                self._invalidlabel['text'] = "Invalid input: another player already has the name %s." % item.name
                self._invalidlabel.pack()
                return
        self._addplayerbutton['state'] = NORMAL
        self._validlabel.pack()
        if self._cpuentry.get() == 1:
            self._world.createPlayer(self._playername.get(), self._riskentry.get(), self._pbentry.get(), self._verboseentry.get())
        else:
            print('verbose', self._verboseentry.get())
            self._world.createPlayer(self._playername.get(), self._verboseentry.get())

    def toggleCpuOptions(self):
        """If the cpu checkbox is checked, show the cpu options. If the cpu checkbox is unchecked, hide the cpu options."""
        if self._cpuentry.get() == 1:
            self._difficultyslider.pack()
            self._riskslider.pack()
            self._pbcheckbox.pack()
        else:
            self._difficultyslider.pack_forget()
            self._riskslider.pack_forget()
            self._pbcheckbox.pack_forget()

    def printcpuvalues(self):
        """Prints the values of the input for the cpu options. This method used for debugging only."""
        print('difficulty:', self._difficultyentry.get(), 'risk:', self._riskentry.get(), 'pb:', self._pbentry.get(),
              'verbose:', self._verboseentry.get())

class worldStats:
    def __init__(self, world, master=None):
        self._world = world
        self._window = master
        self._players = []

    def showWorld(self):
        for player in self._world.getPlayerList():
            print(player.name)
            print(player.gethandlength())
            self._players.append([player, Label(self._window,text=player.name), Label(self._window, text=str(player.gethandlength()) + 'cards')])
        for idx in range(len(self._players)):
            self._players[idx][1].grid(column=idx, row=0)
            self._players[idx][2].grid(column=idx, row=1)
if unit2:
    thisWorld = World()
    root = Tk()
    setupwindow = SetupWidget(world=thisWorld, master=root)
    root.mainloop()
    thisWorld._deck.addAllCards()
    thisWorld.deal()
    master = Tk()
    stats = worldStats(thisWorld, master)
    stats.showWorld()
    master.mainloop()

if unit_tests:
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