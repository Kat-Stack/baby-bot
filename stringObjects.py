class customObject(object):
    totalCount = 0
    totalValue = 0
    myStr = ""

    def __init__(self, val):
        self.totalCount += 1
        self.myStr = val

    def __add__(self, other):
        self.totalValue += other

    def count(self):
        self.totalCount += 1


class wordObject(customObject):

    def __init__(self, string, totalWords):
        super().__init__(string)
        self.update(totalWords)

    def update(self, totalWords):
        self.totalCount += 1
        self.totalValue = self.totalCount/totalWords


class charObject(customObject):

    def __init__(self, strVal, numVal = 1):
        if len(strVal) == 1:
            super().__init__(strVal)
        self.count()
        self.__add__(numVal)

    def __add__(self, other):
        super(charObject, self).__add__(other)


class strObject(customObject):
    contained_chars = {}

    def __init__(self, string, charDict):
        super().__init__(string)
        for char in string:
            if char not in charDict:
                pass


