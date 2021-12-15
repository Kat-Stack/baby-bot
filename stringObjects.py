class customObject(object):
    totalCount = 0
    totalValue = 0
    myStr = ""

    def __init__(self, val, totalWords):
        self.myStr = val
        self.calculate(totalWords)
        self.nextWordDict = {}
        self.prevWordDict = {}

    def calculate(self, totalWords):
        self.count()
        self.totalValue = self.totalCount/totalWords
        return self.totalValue

    def count(self):
        self.totalCount += 1


    def addToNext(self, nextWord):
        if nextWord not in self.nextWordDict:
            self.nextWordDict[nextWord] = 0
        self.nextWordDict[nextWord] += 1

    def addToPrev(self, prevWord):
        if prevWord not in self.prevWordDict:
            self.prevWordDict[prevWord] = 0
        self.prevWordDict[prevWord] += 1
        prevWord.addToNext(self)


class wordObject(customObject):

    def __init__(self, string, totalWords):
        super().__init__(string, totalWords)


    def update(self, totalWords):
        self.totalCount += 1
        self.totalValue = self.totalCount/totalWords

    def getStr(self):
        return self.myStr


class multiWordObject(customObject):

    def __init__(self, listOfWords, totalWords):
        self.wordIndexDict  = {}
        string = ""
        for item in range(0, len(listOfWords)-1):
            self.wordIndexDict[item] = listOfWords[item]
            string += str(listOfWords[item]) + " "
        super().__init__(string, totalWords)

    def calculate(self, totalWords):
        self.count()
        self.totalValue = self.totalCount / totalWords
        multiplied = 1
        for item in self.wordIndexDict.keys():
            multiplied *= self.wordIndexDict[item].calculate(totalWords)
        return multiplied * self.totalValue