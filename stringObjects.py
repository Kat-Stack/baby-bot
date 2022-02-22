from scipy.stats import entropy

class customObject(object):
    totalCount = 0
    totalValue = 0
    myStr = ""

    def __init__(self, val, totalWords):
        self.myStr = val
        self.calculate(totalWords)
        self.totalWords = totalWords

    def calculate(self, totalWords):
        self.count()
        self.totalValue = 1 - (self.totalCount / totalWords)
        return self.totalValue

    def count(self):
        self.totalCount += 1


class wordObject(customObject):

    def __init__(self, string, totalWords):
        super().__init__(string, totalWords)
        self.nextWordDict = {}
        self.prevWordDict = {}

    def update(self, totalWords):
        self.totalCount += 1
        self.totalValue = self.totalCount / totalWords

    def addToNext(self, nextWord):
        if nextWord not in self.nextWordDict:
            self.nextWordDict[nextWord] = 0
        self.nextWordDict[nextWord] = nextWord.calculate(self.totalWords)

    def calculate(self, totalWords):
        self.count()
        self.totalValue = 1 - (self.totalCount / totalWords)
        return self.totalValue

    def addToPrev(self, prevWord):
        if prevWord not in self.prevWordDict:
            self.prevWordDict[prevWord] = 0
        self.prevWordDict[prevWord] += prevWord.calculate(self.totalWords)
        prevWord.addToNext(self)

    def getStr(self):
        return self.myStr + " "


class multiWordObject(customObject):

    def __init__(self, listOfWords, totalWords):
        self.nextWordDict = {}
        self.prevWordDict = {}
        self.wordIndexList = listOfWords
        self.totalWords = totalWords
        self.totalValue = 1
        string = ""
        for item in range(0, len(listOfWords)):
            if item is not len(listOfWords):
                string += str(listOfWords[item].getStr())
            else:
                string += str(listOfWords[item].getStr())
            self.totalValue *= listOfWords[item].calculate(totalWords)
        super().__init__(string, totalWords)

    def addToNext(self, nextWord):
        if nextWord not in self.nextWordDict:
            self.nextWordDict[nextWord] = 0
        self.nextWordDict[nextWord] = nextWord.calculate(self.totalWords)

    def addToPrev(self, prevWord):
        if prevWord not in self.prevWordDict:
            self.prevWordDict[prevWord] = 0
        self.prevWordDict[prevWord] += prevWord.calculate(self.totalWords)
        prevWord.addToNext(self)

    def calculate(self, totalWords):
        self.count()
        multiplied = 1
        self.totalValue = 1
        for item in range(0, len(self.wordIndexList)-1):
            if item == 0:
                self.totalValue *= self.wordIndexList[item].calculate(totalWords)
            else:
                try:
                    self.totalValue *= self.wordIndexList[item - 1].nextWordDict[self.wordIndexList[item]]
                except Exception as e:
                    print("word: {} string objects issue at 85 not in nextWordDict for word {}".format(self.wordIndexList[item].getStr(), e))
        return 1-(multiplied * self.totalValue)

    def getStr(self):
        return self.myStr

class multimultiword(customObject):

    def __init__(self, multiwords, totalWords):
        pass
