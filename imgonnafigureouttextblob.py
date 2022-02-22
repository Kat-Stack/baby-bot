import os
os.environ['APPDATA'] = r"C:\Users\kakeb\AppData\Roaming"
from textblob import TextBlob #ngrams, lang processing, etc. I would rec reading through docs for this
import random
import itertools #iterate through two dicts at same time
import collections #get access to defaultdict type (defaults to key vs throwing keyErrorr like reg dict)








#NOTES STARTED HERE, THEN CODE WAS ADDED ABOVE
#bot class to handle word storage in ram
class Bot:

    def __init__(self, ngramSize=4):
        self.indx = {}
        self.ngramSize = ngramSize

    def addIndex(self, noun_group, ngramDictionary):

        Cdict = collections.defaultdict(int) #(int) defaults the key to 0 if it doesnt exist
        Cdict.setdefault(1)

        if str(noun_group) not in self.indx:
            self.indx[str(noun_group)] = {}

        counter = True #bool to flip flop between handling for the two different dictionaries
        for key, val in itertools.chain(self.indx[str(noun_group)].items(), ngramDictionary.items()): #for every key in both of these, loop through and add em up
            if type(val) is dict:
                if key not in Cdict:
                    Cdict[key] = {}
                if counter: #nested dictionaries to store words and next words
                    for item in ngramDictionary[key]:
                        if item not in Cdict[key]:
                            Cdict[key][item] = 0
                        Cdict[key][item] += 1
                    #counter = False
                else:
                    for item in self.indx[str(noun_group)]:
                        if item not in Cdict[key]:
                            Cdict[key][item] = 0
                        Cdict[key][item] += 1
                    #counter = True
            else:
                Cdict[str(key)] += val

        self.indx[noun_group] = dict(Cdict) #saves the modified dictionary back to the index

    # get a response from a message using the text provided
    def getResponse(self, discordMessage):
        blob = TextBlob(discordMessage)
        blobNounPhrases = blob.noun_group
        self.loadToCorpus(blob, blobNounPhrases)
        response = self.genResponse(blob, blobNounPhrases)
        return response


    #gen a response based on current brain
    def genResponse(self, blob, blobNounPhrases):
        currentBrain = {}
        Cdict = collections.defaultdict(int)  # (int) defaults the key to 0 if it doesnt exist
        Cdict.setdefault(1)
        for item in blobNounPhrases:
            for key, val in itertools.chain(self.indx[item].items()):  # for every key in both of these, loop through and add em up
                if key != 1:
                    pass




    # load to brain
    def loadToCorpus(self, blob, blobNounPhrases):
        ngramsDictToBeLoadedIntoIndex = self.processNgrams(blob.ngrams(self.ngramSize))
        for item in blobNounPhrases:
            self.addIndex(str(item), ngramsDictToBeLoadedIntoIndex)
        return str(self.indx)

    #compile the ngrams and return for a response
    def compileNgrams(self, blob):
        Cdict = collections.defaultdict(int)  # (int) defaults the key to 0 if it doesnt exist
        Cdict.setdefault(1)

        for item in blob:
            if item in self.indx:
                for key, val in itertools.chain(self.indx[item]):
                    Cdict[key] += val


        return dict(Cdict)


    #process the ngrams into a dictionary
    def processNgrams(self, ngramList):
        counter = 4
        ngrams_and_next = {}
        tempList = {}
        pass_go = False
        newDict = {}
        for item in ngramList:
            if pass_go:
                ngrams_and_next[str(tempList[counter])] = str(item[0])
            else:
                if counter == self.ngramSize-1:
                    pass_go = True
            tempList[counter] = item
            if counter >= self.ngramSize:
                counter = 1
            else:
                counter += 1


        for item in ngrams_and_next:
            item = str(item)
            if item not in newDict:
                newDict[item] = {str(ngrams_and_next[item]): 0}
            newDict[item][str(ngrams_and_next[item])] += 1

        return newDict