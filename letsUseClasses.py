import stringObjects
import random

totalWordTracker = [1, {}] # [totalCount of words, {dictionary with all words and counts}
lastTrackedWord = ""
multiWordStarts = {}

#handles the response system from input to output. Controller type deal
def getResponse(messageTOTAL):
    message = messageTOTAL.content
    out = ""
    try:
        starter = random.choice(processMessage(message)) #calls processMessage to input to corpus. Recieves a list of every word and picks a random one to start responding with
        lastWord = crawlCorpusForNext(totalWordTracker[1][starter])
        for i in range(1, random.randint(2,50)):
            nextWord = crawlCorpusForNext(lastWord)
            out += " " + lastWord.getStr()
            lastWord = nextWord
    except:
        if len(multiWordStarts) > 2 and out == "":
            out = str(random.choice(list(multiWordStarts.keys())))
            return out
        elif out == "":
            out = message
            return out
        else:
            return out

    return out

def assignToAuthor(messageTOTAL):
    fileName = "people/" + str(messageTOTAL.author)
    with open(fileName, "a+", encoding="utf-8") as f:
        f.write(messageTOTAL.content + "\n")
        processMessage(messageTOTAL.content)

#processes the message into wordObjects
def processMessage(message):
    global totalWordTracker
    global lastTrackedWord
    global multiWordStarts
    listOfResponse = []
    #if the message is longer than one word
    if len(message.split(" ")) > 1:
        #for every word in the list
        multiWordList = []
        for word in message.split(" "):
            totalWordTracker[0] += 1
            if word not in totalWordTracker[1]:
                newWord = stringObjects.wordObject(word, totalWordTracker[0])
                totalWordTracker[1][word] = newWord
            else:
                totalWordTracker[1][word].update(totalWordTracker[0])
            if 0 < list.index(message.split(" "), word):
                totalWordTracker[1][word].addToPrev(
                    totalWordTracker[1][message.split(" ")[list.index(message.split(" "), word) - 1]])
            listOfResponse.append(word)
            if list.index(message.split(" "), word) == len(message.split(" "))-1:
                lastTrackedWord = totalWordTracker[1][word]
            if lastTrackedWord in totalWordTracker and list.index(message.split(" "), word) == 0:
                totalWordTracker[1][word].addToPrev(totalWordTracker[1][lastTrackedWord])
            multiWordList.append(totalWordTracker[1][word])
        multiWord = stringObjects.multiWordObject(multiWordList, totalWordTracker[0])
        multiWordStarts[message] = multiWord



    else:
        newWord = stringObjects.wordObject(message, totalWordTracker[0])
        totalWordTracker[1][message] = newWord
        listOfResponse.append(message)
    return listOfResponse

def crawlCorpusForNext(lastWord):
    if len(lastWord.nextWordDict) == 0:
        nextWord = max(zip(lastWord.prevWordDict.values(), lastWord.prevWordDict.keys()))[1]
    else:
        randNum = random.randint(0,100)
        if randNum > 70:
            nextWord = random.choice(list(lastWord.nextWordDict.keys()))
        else:
            nextWord = max(lastWord.nextWordDict, key=lastWord.nextWordDict.get)

    return nextWord


#devours the text from a text file
def eatTextFiles(file):
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            for finalSplit in line.replace("\n", ".").split("."):
                processMessage(finalSplit)


#adds multiple text files to a corpus
def addToCorpus(corpusTextFile):
    with open(corpusTextFile, encoding='utf-8') as f:
        for item in f:
            eatTextFiles(item.strip("\n"))


def saveToInteractions(messageTotal):
    pass

#this class needs to be written later
def makeDecision():
    pass
#this function will choose which response we get. I want it to try and match the entropy level of whatever response it got.

#Will need to figure out if it should use big series of words or teeeny tiny ones. Probably start with bigger length words and work way down