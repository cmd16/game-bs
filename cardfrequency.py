"""A class to keep track of how many of each card number a player has"""
debugging = True
class CardFreq:
    """A class to keep track of how many of each card number a player has"""
    def __init__(self, player, verbose=False, logfile=None):
        """Create self with an empty list"""
        self.freq_list = []
        self.player = player
        self.verbose = verbose
        self.log = logfile

    def updateSelf(self):
        """Create or update the card frequency list. Called every time a player is about to play."""
        if self.verbose:
            print(self.player.name + "'s CardFreq updating self")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq updating self")
        self.freq_list = []  # reset the list
        card_num_list = [x.get_number() for x in
                         self.player.hand]  # create a list to hold the cards and how many of each card there is
        if self.verbose:
            print(self.player.name + "'s card num list is: " + str(card_num_list))
        if self.log is not None:
            self.log.write(self.player.name + "'s card num list is: " + str(card_num_list))
        for num in range(1, 15):
            count = card_num_list.count(num)
            if 0 < count <= self.player.risk:
                self.freq_list.append([num, count])  # append the number of the card and the frequency of that card
        if len(self.freq_list) == 0:  # if there aren't any cards with a low enough frequency, just get all the cards
            if self.verbose:
                print(self.player.name + "'s CardFreq found no cards with frequency less than or equal to risk level")
            if self.log is not None:
                self.log.write(self.player.name + "'s CardFreq found no cards with frequency less than or equal to risk level")
            for num in range(1, 15):
                count = card_num_list.count(num)
                if count > 0:
                    self.freq_list.append([num, count])
        if self.verbose:
            print(self.player.name + "'s CardFreq list: " + str(self))
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq list: " + str(self))

    def getMostFreq(self):
        """Return the number and frequency of the card that the player has the most of"""
        if self.verbose:
            print(self.player.name + "'s CardFreq returning the number and frequency of the card that the player has the most of")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq returning the number and frequency of the card that the player has the most of")
        high_num = 0
        high_couples = []
        for couple in self.freq_list:
            if couple[1] >= high_num:
                high_num = couple[1]
                high_couples.append(couple)
        if self.verbose:
            print(self.player.name + "'s CardFreq high couples: " + str(high_couples))
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq high couples: " + str(high_couples))
        return high_couples

    def getLeastFreq(self):
        """Return the number and frequency of the card that the player has the least of"""
        if self.verbose:
            print(self.player.name + "'s CardFreq looking for the number and frequency of the card that the player has the least of")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq looking for the number and frequency of the card that the player has the least of")
        low_num = 5
        low_couples = None
        for couple in self.freq_list:
            if couple[1] <= low_num:
                low_num = couple[1]
                low_couples.append(couple)
        if self.verbose:
            print(self.player.name + "'s CardFreq low couples: " + str(low_couples))
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq low couples: " + str(low_couples))
        return low_couples

    def getNotNextHonest(self):
        """Find the next card that the player will be able to honestly play, then return the frequency list without that card"""
        if self.verbose:
            print(self.player.name + "'s CardFreq looking for the next card that the player will be able to honestly play")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq looking for the next card that the player will be able to honestly play")
        if len(self.freq_list) == 1:
            return self.freq_list
        next_nums = self.player.getNextNumbers()
        modified_list = self.freq_list[:]
        for num in next_nums:
            item = self.getNum(num)
            if item:  # all non-False, non-zero values are "truthy"
                modified_list.remove(item)
                break
        return modified_list

    def getLeastNotNextHonest(self):
        """Find the card that the player has the least of that they won't play next."""
        if self.verbose:
            print(self.player.name + "'s CardFreq looking for the card that the player has the least of that they won't play next")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq looking for the card that the player has the least of that they won't play next")
        low_num = 5
        low_couples = None
        for couple in self.getNotNextHonest():
            if couple[1] <= low_num:
                low_num = couple[1]
                low_couples.append(couple)
        if self.verbose:
            print(self.player.name + "'s CardFreq low not next couples: " + str(low_couples))
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq low not next couples: " + str(low_couples))
        return low_couples

    def getLastHonest(self):
        """Find the last card that the player will be able to honestly play, then return that number and frequency"""
        if self.verbose:
            print(self.player.name + "'s CardFreq looking for the last card that the player will be able to honestly play")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq looking for the last card that the player will be able to honestly play")
        next_nums = self.player.getNextNumbers()
        if debugging:
            print("debugging next nums:", next_nums)
        for idx in range(-1, - len(next_nums) - 1, -1):
            next_num = next_nums[idx]
            item = self.getNum(next_num)
            if debugging:
                print('debugging idx:', idx, "debugging num", next_num, "debugging item:", item)
            if item:
                if self.verbose:
                    print(self.player.name + "'s CardFreq found the last item: " + str(item))
                if self.log is not None:
                    self.log.write(self.player.name + "'s CardFreq found the last item: " + str(item))
                return item

    def returnItemList(self):
        """Return the frequency list"""
        if self.verbose:
            print(self.player.name + "'s CardFreq returning the list")
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq returning the list")
        return self.freq_list

    def getNum(self, num):
        """Searches the frequency list for the given number. If found, return the number and frequency. Else, return False."""
        if self.verbose:
            print(self.player.name + "'s CardFreq looking for " + str(num))
        if self.log is not None:
            self.log.write(self.player.name + "'s CardFreq looking for " + str(num))
        for couple in self.freq_list:
            if couple[0] == num:
                if self.verbose:
                    print(self.player.name + "'s CardFreq found " + str(couple))
                if self.log is not None:
                    self.log.write(self.player.name + "'s CardFreq found " + str(couple))
                return couple
        return False

    def __str__(self):
        """Return a string representation of self's frequency list"""
        return str(self.freq_list)
