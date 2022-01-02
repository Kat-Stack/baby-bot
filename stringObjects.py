class customObject(object):
    totalCount = 0
    totalValue = 0
    myStr = ""
    nextWordDict = {}
    prevWordDict = {}
    nextWordDictValues = {}
    lastKnownTotalWords = 0

    def __init__(self, val, totalWords):
        self.myStr = val
        self.lastKnownTotalWords = totalWords
        self.calculate(totalWords)


    def calculate(self, totalWords):
        self.count()
        self.totalValue = self.totalCount/totalWords
        self.lastKnownTotalWords = totalWords
        return self.totalValue

    def count(self):
        self.totalCount += 1

    def addToNext(self, nextWord):
        if nextWord not in self.nextWordDict:
            self.nextWordDict[nextWord] = 0
            self.nextWordDictValues[nextWord] = 0
        self.nextWordDict[nextWord] += 1
        if self.lastKnownTotalWords == 0:
            print("issue with totalWords on {}".format(nextWord.getStr()))
            self.lastKnownTotalWords = nextWord.lastKnownTotalWords
        self.nextWordDictValues[nextWord] = self.nextWordDict[nextWord] / max(self.nextWordDict.values()) + nextWord.calculate(self.lastKnownTotalWords)

    def addToPrev(self, prevWord):
        if prevWord not in self.prevWordDict:
            self.prevWordDict[prevWord] = 0
        self.prevWordDict[prevWord] += 1
        prevWord.addToNext(self)

    def getNextWordDict(self):
        return self.nextWordDict

    def getStr(self):
        return self.myStr

    def update(self, totalWords):
        self.totalCount += 1
        self.totalValue = self.totalCount/totalWords
        self.lastKnownTotalWords = totalWords


class wordObject(customObject):

    def __init__(self, string, totalWords):
        super().__init__(string, totalWords)







class multiWordObject(customObject):
    lastKnownTotalWords = 0

    def __init__(self, listOfWords, totalWords):
        self.lastKnownTotalWords = totalWords
        self.wordIndexDict  = {}
        string = ""
        for item in range(0, len(listOfWords)):
            self.wordIndexDict[item] = listOfWords[item]
            string += str(listOfWords[item].getStr()) + " "
            if item == len(listOfWords)-1:
                if self.wordIndexDict[item].getNextWordDict() != {}:
                    for each in self.wordIndexDict.keys():
                        self.wordIndexDict[each].addToPrev(self)
        if len(listOfWords) == 1:
            string = listOfWords[0].getStr()
        super().__init__(string, totalWords)

    def calculate(self, totalWords):
        self.count()
        self.totalValue = self.totalCount / totalWords
        multiplied = 1
        if len(self.wordIndexDict.keys()) > 800:
            multiplied = 1
            print("almost broke via recursion on {}".format(self.getStr()))
        else:
            for item in self.wordIndexDict.keys():
                multiplied *= self.wordIndexDict[item].calculate(totalWords)
        return multiplied