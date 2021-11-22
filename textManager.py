import random
import nodesr as n
import re

corpusBodySource = "corpusBodySource"
CORPUSBODY = []
# ("empty", "interactions.txt", "voaEnglish", "avatar", "got", "redditCorpus") ("empty", "sample")

corpus = """"""
wordTagDict = {}
tagCorpusDict = {}
ngram = {}
corpusDict = {}
wordLinkedListDict = {}
db = {}


def getCorpus():
    return corpus


def populateCorpus(corpusBody=CORPUSBODY):
    global corpus
    global ngram
    global CORPUSBODY
    corpusBody = CORPUSBODY
    with open(corpusBodySource) as file:
        for item in file.readlines():
            corpusBody.append(item.strip("\n"))
    for item in corpusBody:
        corpusList = []
        with open("newCorpus/" + item, encoding="utf-8") as file:
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


def getResponse(message, interactionsFile="newCorpus/interactions.txt"):
    global ngram
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

    write = "INITIAL MESSAGE: " + message + "MY RESPONSE: " + out + "\n"
    f = open(interactionsFile, "a", encoding="utf-8")
    processMessage(message)
    f.write(write)
    processMessage(out)
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


# taking out for a bit
def populaterCorpus(corpusBody=CORPUSBODY):
    global corpus
    global ngram
    for item in corpusBody:
        corpusDict = {}
        corpusList = []
        with open("newCorpus/" + item, encoding="utf-8") as file:
            corpusList += file.readlines()
        for items in corpusList:
            if items not in corpusDict:
                corpusDict[items.replace('"', ' ').replace('\n', ' ').replace('[', ' ').replace(']', ' ')] = []
        for sentence in corpusDict.keys():
            linkedNodeList = n.LinkedList()
            splitSentence = sentence.split(" ")
            for i in range(1, len(splitSentence) + 1):
                node = n.Node(splitSentence[i - 1])
                linkedNodeList.insert(node)
                if wordLinkedListDict.get(splitSentence[i - 1]):
                    wordLinkedListDict[splitSentence[i - 1]].append(linkedNodeList)
                else:
                    thisIsaList = []
                    linkedNodeListSequence = linkedNodeList.printBackwards(thisIsaList)
                    tempList = []
                    for item in linkedNodeListSequence:
                        item.printLL()
                        tempList.append(item)
                    wordLinkedListDict[splitSentence[i - 1]] = tempList


#              if '' in node.data:
#                  continue
#           if (linkedNodeList) not in ngram:
#              ngram[linkedNodeList] = []
#               thisIsaList = []
#                linkedNodeListSequence = linkedNodeList.printBackwards(thisIsaList)
#                 for item in linkedNodeListSequence:
#                    ngram[item].append(splitSentence[i-1])

# taking out for a bit
def getrResponse(message):
    out = ""
    outMinusIDK = ""
    # processedMessage is a list of the message that was sent in a discord chat.
    processedMessage = processMessage(message)
    if int(len(processedMessage)) > 1:
        # thisManyLengths = how many responses babyBot should gives
        thisManyLengths = int(len(processedMessage) / 2)
    else:
        thisManyLengths = 1
    for i in range(thisManyLengths):
        linkedListWord = random.choice(processedMessage)
        if wordLinkedListDict.get(linkedListWord):
            # this shouldn't be random eventually. Eventually we want the bot to decide which context is best using tags
            outMinusIDK += random.choice(wordLinkedListDict[linkedListWord]).getLL()
            out += random.choice(wordLinkedListDict[linkedListWord]).getLL() + "??????"
        else:
            # with the changes I have made in the morning of 11.15 this will no longer be hit. ProcessMessage now saves the response to ngram list so this logic will never hit false
            out += " I do not know what {} means ".format(linkedListWord)

            # while True:
            #   if linkedList not in ngram.keys():
            #      break
            # third = random.choice(list(ngram[linkedList]))
            # if ngram.get(third):
            # out += ngram.get(third).getLL() + ' '

    #        word_pair = (third[1], third)

    f = open("newCorpus/interactions.txt", "a")
    f.write(message + " " + "\n" + out + "\n")
    f.close()

    return out


def corpusInit(corpusBody=CORPUSBODY):
    populateCorpus(corpusBody)


def processrMessage(message):
    messageList = list()
    messageList = message.split(" ")
    splitSentence = message.split(' ')
    for i in range(1, len(splitSentence) + 1):
        linkedNodeList = n.LinkedList()
        node = n.Node(splitSentence[i - 1])
        linkedNodeList.insert(node)
        if wordLinkedListDict.get(splitSentence[i - 1]):
            wordLinkedListDict[splitSentence[i - 1]].append(linkedNodeList)
        else:
            thisIsaList = []
            linkedNodeListSequence = linkedNodeList.printBackwards(thisIsaList)
            tempList = []
            for item in linkedNodeListSequence:
                additionalTempList = []
                additionalTempList.append(item)
                print(item.getLL())
                tempList.append(item)
                if wordLinkedListDict.get(splitSentence[i - 1]):
                    wordLinkedListDict[splitSentence[i - 1]] = wordLinkedListDict.get(splitSentence[i - 1]).append(item)
                else:
                    wordLinkedListDict[splitSentence[i - 1]] = tempList
                    wordLinkedListDict[splitSentence[i - 1]] = additionalTempList
    #      tempList = list()
    #       tempList.append(linkedNodeList)
    #     wordLinkedListDict[splitSentence[i - 1]] = tempList

    #              if '' in node.data:
    #                  continue
    #   if (linkedNodeList) not in ngram:
    #      ngram[linkedNodeList] = []
    #       thisIsaList = []
    #        linkedNodeListSequence = linkedNodeList.printBackwards(thisIsaList)
    #         for item in linkedNodeListSequence:
    #            ngram[item].append(splitSentence[i-1])
    return messageList
