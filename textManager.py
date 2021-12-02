import random
import nodesr as n
import re
from discord.ext import commands
import entropy

corpusBodySourceFile = "corpusBodySource"
CORPUSBODY = []
# ("empty", "interactions.txt", "voaEnglish", "avatar", "got", "redditCorpus") ("empty", "sample")

corpus = """"""
wordTagDict = {}
tagCorpusDict = {}
#text then number is text, number then text is serializedDict
ngram1 = "pickles/oneNgram"
ngram2 = "pickles/twoNgram"
ngram3 = "pickles/twoNgram"
ngram4 = "pickles/twoNgram"
ngram5 = "pickles/twoNgram"
corpusDict = {}
wordLinkedListDict = {}
db = {}
alreadyReadCorpi = []
alreadyReadCorpiLocation = "activeUse/alreadyRead"
alreadyReadFLAG = True


def getCorpus():
    return corpus


def populateCorpus(corpusBodySource, readFlag=True):
    global ngram1
    global ngram2
    global ngram3
    global ngram4
    global ngram5
    global CORPUSBODY

    global alreadyReadCorpiLocation
    global alreadyReadCorpi
    alreadyReadCorpi = []
    corpusBody = []
    corpus = ""
    if not readFlag:
        ngram1, ngram2, ngram3, ngram4, ngram5 = entropy.readNgramsData(ngram1, ngram2, ngram3, ngram4, ngram5)
    with open(alreadyReadCorpiLocation, encoding="utf-8") as f:
        for item in f:
            alreadyReadCorpi.append(item.strip("\n"))
    with open(str(corpusBodySource), encoding="utf-8") as file:
        for item in file.readlines():
            if alreadyReadCorpi.__contains__(item.strip("\n")):
                pass
            else:
                corpusBody.append(item.strip("\n"))
    for item in corpusBody:
        if alreadyReadCorpi.__contains__(item):
            pass
        else:
            corpusList = []
            with open(item, encoding="utf-8") as file:
                corpusList += file.readlines()
            for items in corpusList:
                corpus += items
            alreadyReadCorpi.append(item.strip("\n"))
    with open(alreadyReadCorpiLocation, "w", encoding="utf-8") as f:
        for item in alreadyReadCorpi:
            f.write(item.strip("\n") + "\n")
    corpus = corpus.replace('\n', '.')
    for sentence in re.split('[!.?,\t\n]', corpus):
        entropy.ngramManager(sentence, ngram1, ngram2, ngram3, ngram4, ngram5)


def getResponse(messageTOTAL, interactionsFile="newCorpus/interactions.txt"):
    if not alreadyReadFLAG:
        populateCorpus([interactionsFile, ], False)
    message = messageTOTAL.content
    author = messageTOTAL.author

    out = entropy.getResponse(ngram2, message)
    processMessage(message)
    processMessage(out)
    return out


def grabATempDict(message):
    tempDict = {}
    if len(message.split(' ')) > 1:

        for i in range(1, len(message.split(' '))):
            word_pair = (message.split(' ')[i - 2], message.split(' ')[i - 1])
            if '' in word_pair:
                continue
            elif (word_pair) not in tempDict:
                tempDict[word_pair] = []
            tempDict[word_pair].append(message.split(' ')[i])
        return tempDict


def processMessage(sentence):
    global ngram1
    for i in range(1, len(sentence.split(' '))):
        word_pair = (sentence.split(' ')[i - 2], sentence.split(' ')[i - 1])
        if '' in word_pair:
            continue
        if word_pair not in ngram1:
            ngram1[word_pair] = []
        ngram1[word_pair].append(sentence.split(' ')[i])


def addWords(dictionar, word_pair, stringValue):
    dictionar[word_pair][0] += 1
    tempDict = dictionar[word_pair][1]  # this is just for readability. we don't use this, we hard code it in
    if stringValue not in dictionar[word_pair][1]:
        dictionar[word_pair][1][stringValue] = 0
    dictionar[word_pair][1][stringValue] += 1


# pass in a sentence, saves to DB as sequences
def sendToDB(sentence):
    wordList = sentence.split(" ")
    for i in range(0, len(wordList) + 1):
        if db.get(wordList[i - 1]) and len(wordList) > i:
            db[wordList[i - 1]] = db[wordList[i - 1]].append(wordList[i])
        elif len(wordList) > i:
            thisList = []
            thisList.append(wordList[i])
            db[wordList[i - 1]] = thisList


def corpusInit(corpusBody=corpusBodySourceFile, readFlag=True):
    if type(corpusBody) == str:
        populateCorpus(corpusBody, readFlag)
    elif type(corpusBody) == tuple:
        populateCorpus(corpusBody[0], readFlag)
    else:
        for item in corpusBody:
            if type(item) == tuple:
                populateCorpus(item[0], readFlag)
            else:
                populateCorpus(item, readFlag)
