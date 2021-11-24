import random
import nodesr as n
import re
from discord.ext import commands

corpusBodySourceFile = "corpusBodySource"
CORPUSBODY = []
# ("empty", "interactions.txt", "voaEnglish", "avatar", "got", "redditCorpus") ("empty", "sample")

corpus = """"""
wordTagDict = {}
tagCorpusDict = {}
ngram = {}
corpusDict = {}
wordLinkedListDict = {}
db = {}
ngram2 = {}


def getCorpus():
    return corpus


def populateCorpus(corpusBodySource):
    global ngram
    global CORPUSBODY
    global ngram2
    corpusBody = []
    corpus = ""
    with open(str(corpusBodySource)) as file:
        for item in file.readlines():
            corpusBody.append(item.strip("\n"))
    for item in corpusBody:
        corpusList = []
        with open(item, encoding="utf-8") as file:
            try:
                corpusList += file.readlines()
            except UnicodeDecodeError:
                pass
        for items in corpusList:
            corpus += items
    corpus = corpus.replace('\n', '.')
    for sentence in re.split('[!.?,\t\n]', corpus):
        for i in range(1, len(sentence.split(' '))):
            word_pair = (sentence.split(' ')[i - 2], sentence.split(' ')[i - 1])
            if '' in word_pair:
                continue
            if word_pair not in ngram:
                ngram[word_pair] = []
            ngram[word_pair].append(sentence.split(' ')[i])





def getResponse(messageTOTAL, interactionsFile="newCorpus/interactions.txt"):
    global ngram
    message = messageTOTAL.content
    author = messageTOTAL.author
    try:
        tempDict = grabATempDict(message)
    except UnicodeDecodeError:
        tempDict = ngram
    if bool(tempDict):
        word_pair = random.choice(list(tempDict.keys()))
    else:
        word_pair = random.choice(list(ngram.keys()))
    out = word_pair[0] + ' ' + word_pair[1] + ' '

    while True:
        if word_pair not in ngram.keys() or word_pair[1] == ngram[word_pair] or word_pair[0] == ngram[word_pair]:
            break
        if len(out) > 1000:
            break
        third = random.choice(list(ngram[word_pair]))
        out += third + ' '
        word_pair = (word_pair[1], third)

    write = "Q: " + message + "A: " + out + "\n"
    userFile = open("peopleiknow/"+str(author)+".txt", "a", encoding="utf-8")
    f = open(interactionsFile, "a", encoding="utf-8")
    processMessage(message)
    userFile.write(write)
    f.write(write)
    processMessage(out)
    userFile.close()
    f.close()
    return out

def grabATempDict(message):
    tempDict = {}
    if len(message.split(' ')) > 1:

        for i in range(1, len(message.split(' '))):
            word_pair = (message.split(' ')[i - 2], message.split(' ')[i-1])
            if '' in word_pair:
                continue
            elif (word_pair) not in tempDict:
                tempDict[word_pair] = []
            tempDict[word_pair].append(message.split(' ')[i])
        return tempDict

def processMessage(sentence):
    global ngram
    for i in range(1, len(sentence.split(' '))):
        word_pair = (sentence.split(' ')[i - 2], sentence.split(' ')[i-1])
        if '' in word_pair:
            continue
        if word_pair not in ngram:
            ngram[word_pair] = []
        ngram[word_pair].append(sentence.split(' ')[i])


def addWords(dictionar, word_pair, stringValue):
    dictionar[word_pair][0] += 1
    tempDict = dictionar[word_pair][1] #this is just for readability. we don't use this, we hard code it in
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



def corpusInit(corpusBody=corpusBodySourceFile):
    if type(corpusBody) == str:
        populateCorpus(corpusBody)
    elif type(corpusBody) == tuple:
        populateCorpus(corpusBody[0])
    else:
        for item in corpusBody:
            if type(item) == tuple:
                populateCorpus(item[0])
            else:
                populateCorpus(item)

