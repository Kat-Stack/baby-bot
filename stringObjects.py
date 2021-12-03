class customObject(object):
    totalCount = 0
    totalValue = 0
    myStr = ""

    def __init__(self, val, totalWords):
        self.totalCount += 1
        self.myStr = val
        self.calculate(totalWords)

    def calculate(self, totalWords):
        self.totalValue = self.totalCount/totalWords

    def count(self):
        self.totalCount += 1


class wordObject(customObject):

    def __init__(self, string, totalWords):
        super().__init__(string, totalWords)
        self.nextWordDict = {}
        self.prevWordDict = {}

    def update(self, totalWords):
        self.totalCount += 1
        self.totalValue = self.totalCount/totalWords

    def addToNext(self, nextWord):
        if nextWord not in self.nextWordDict:
            self.nextWordDict[nextWord] = 0
        self.nextWordDict[nextWord] += 1

    def addToPrev(self, prevWord):
        if prevWord not in self.prevWordDict:
            self.prevWordDict[prevWord] = 0
        self.prevWordDict[prevWord] += 1
        prevWord.addToNext(self)

    def getStr(self):
        return self.myStr