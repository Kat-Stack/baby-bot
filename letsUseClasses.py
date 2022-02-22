import stringObjects
import random
from scipy.stats import entropy
from textblob import TextBlob


totalWordTracker = [1, {}]  # [totalCount of words, {dictionary with all words and counts}
lastTrackedWord = ""
multiWordStarts = {}


# handles the response system from input to output. Controller type deal
def getResponse(messageTOTAL, message):
    out = ""
    try: 
        starter = processMessage(
            message)  # calls processMessage to input to corpus. Recieves a list of every word and picks a random one to start responding with
        nextWord = crawlCorpusForNext(totalWordTracker[1][starter])
        for i in range(1, random.randint(2, 50)):
            out += nextWord.getStr() + " "
            lastWord = nextWord
            nextWord = crawlCorpusForNext(lastWord)
    except Exception as e:
        print(e)
        if len(multiWordStarts) > 2 and out == "":
            try:
                starter = str(random.choice(list(multiWordStarts.keys())))
                nextWord = crawlCorpusForNext(totalWordTracker[1][starter])
                for i in range(1, random.randint(2, 50)):
                    out += nextWord.getStr() + " "
                    lastWord = nextWord
                    nextWord = crawlCorpusForNext(lastWord)
                return out
            except Exception as e:
                print("you should know an error lets use classes 31 {}".format(e))
                if out == "":
                    out = message
                return out
    fullSave(messageTOTAL, message)
    return out


# save to channel files
def assignToChannel(messageTOTAL, message):
    fileName = "channels/" + str(messageTOTAL.channel)
    saveToFile(message, fileName)


# save to people files
def assignToAuthor(messageTOTAL, message):
    fileName = "people/" + str(messageTOTAL.author)
    saveToFile(message, fileName)


# save to server files
def assignToServer(messageTOTAL, message):
    fileName = "server/" + str(messageTOTAL.guild)
    saveToFile(message, fileName)


# saves to file
def saveToFile(string, fileNAME):
    with open(fileNAME, "a+", encoding="utf-8") as f:
        f.write(string + "\n")
        processMessage(string)


# saves to all places
def fullSave(messageTOTAL, message):
    assignToAuthor(messageTOTAL, message)
    assignToChannel(messageTOTAL, message)
    assignToServer(messageTOTAL, message)


# processes the message into wordObjects
def processMessage(message):
    global totalWordTracker, prevThreePrev, threePrev, prevTwoPrev, twoPrev, prevThreMultiWord, threeMultiWord, multiWord, mostRecent, singleWord, lastWord
    global lastTrackedWord
    global multiWordStarts
    message = ' '.join(message.split())
    # if the message is longer than one word
    splitMessage = message.split((" "))
    if len(splitMessage) > 1:
        twoCounter = 1
        twoList = []
        threeCounter = 2
        threeList = []
        mostRecent = 0
        for word in splitMessage:
            totalWordTracker[0] += 1
            if word not in totalWordTracker[1]:
                newWord = stringObjects.wordObject(word, totalWordTracker[0])
                totalWordTracker[1][word] = newWord
            else:
                totalWordTracker[1][word].update(totalWordTracker[0])
            try:
                totalWordTracker[1][word].addToPrev(totalWordTracker[1][splitMessage[list.index(splitMessage, word) - 1]])
            except Exception as e:
                print("totalwordTracker issues idk {}".format(e))
            if list.index(splitMessage, word) == len(splitMessage) - 1:
                lastTrackedWord = totalWordTracker[1][word]
            if lastTrackedWord in totalWordTracker and list.index(splitMessage, word) == 0:
                totalWordTracker[1][word].addToPrev(totalWordTracker[1][lastTrackedWord])
            mostRecent = 1
            singleWord = totalWordTracker[1][word]

            if twoCounter > 0:
                try:
                    try:
                        totalWordTracker[1][word].addToPrev(totalWordTracker[1][multiWord])
                    except Exception as e:
                        print("issue: {}".format(e))
                    try:
                        totalWordTracker[1][multiWord].addToPrev(totalWordTracker[1][twoPrev])
                    except Exception as e:
                        print("issue: {}".format(e))
                    twoPrev = prevTwoPrev
                    mostRecent = 2
                except Exception as e:
                    print("error in letsUseClasses 2gram connections {}".format(e))
                twoList.append(totalWordTracker[1][word])
                twoCounter -= 1

            else:
                twoList.append(totalWordTracker[1][word])
                twoCounter -= 1
                prevTwoPrev = word
                multiWord = stringObjects.multiWordObject(twoList, totalWordTracker[0])
                multiWordStarts[message] = multiWord
                totalWordTracker[1][multiWord] = multiWord

                twoList = []
                twoCounter = 1

            if threeCounter == 2:
                try:
                    try:
                        totalWordTracker[1][word].addToPrev(totalWordTracker[1][threeMultiWord])
                    except Exception as e:
                        print("issue: {}".format(e))
                    try:
                        totalWordTracker[1][threeMultiWord].addToPrev(totalWordTracker[1][threePrev])
                    except Exception as e:
                        print("issue: {}".format(e))
                    try:
                        totalWordTracker[1][threeMultiWord].addToPrev(totalWordTracker[1][prevThreMultiWord])
                    except Exception as e:
                        print("issue: {}".format(e))
                    threePrev = prevThreePrev
                    prevThreMultiWord = threeMultiWord
                    mostRecent = 3
                except Exception as e:
                    print("error in letsUseClasses 3grams connections{}".format(e))
            if threeCounter > 0:
                threeList.append(totalWordTracker[1][word])
                threeCounter -= 1
            else:
                threeList.append(totalWordTracker[1][word])
                threeCounter -= 1
                prevThreePrev = word
                threeMultiWord = stringObjects.multiWordObject(threeList, totalWordTracker[0])
                multiWordStarts[message] = threeMultiWord
                totalWordTracker[1][threeMultiWord] = threeMultiWord

                threeList = []
                threeCounter = 2

    if mostRecent == 1:
        lastWord = singleWord
    elif mostRecent == 2:
        lastWord = multiWord
    elif mostRecent == 3:
        lastWord = threeMultiWord
    return lastWord


# crawls corpus and grabs next best word / set of words
def crawlCorpusForNext(lastWord):
    if len(lastWord.nextWordDict) == 0:
        nextWord = random.choice(list(lastWord.nextWordDict.keys()))
    else:
        randNum = random.randint(0, 100)
        if randNum > 70:
            nextWord = random.choice(list(lastWord.nextWordDict.keys()))
        else:
            # use min to get the best result
            nextWord = max(entropy(list(lastWord.nextWordDict)), key=lastWord.nextWordDict.get)

    return nextWord


# devours the text from a text file
def eatTextFiles(file):
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()
        messageToLoad = ""
        counter = 0
        numOfBops = 0
        for line in lines:
            if line != " ":
                for finalSplit in line.replace("\n", ".").split("."):
                    messageToLoad += finalSplit + "."
                messageToLoad += " "
                counter += 1
                if counter > 3:
                    processMessage(messageToLoad)
                    counter = 0
                    numOfBops += 1
                    messageToLoad = ""

        processMessage(messageToLoad)


# adds multiple text files to a corpus
def addToCorpus(corpusTextFile):
    with open(corpusTextFile, encoding='utf-8') as f:
        for item in f:
            print("starting {}".format(item))
            eatTextFiles(item.strip("\n"))
            print("finished {}".format(item))


def saveToInteractions(messageTotal):
    pass


# this class needs to be written later
def makeDecision():
    pass
# this function will choose which response we get. I want it to try and match the entropy level of whatever response it got.

# Will need to figure out if it should use big series of words or teeeny tiny ones. Probably start with bigger length words and work way down
