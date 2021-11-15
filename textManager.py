import random
import nodes as n

CORPUSBODY = ("empty", "interactions.txt", "voaEnglish", "avatar", "got")
#"corpus.txt", "avatar.txt", "avatarScenes.txt", "interactions.txt",

corpus = """"""
wordTagDict = {}
tagCorpusDict = {}
ngram = {}
corpusDict = {}
wordLinkedListDict = {}


def getCorpus():
    return corpus


def populateCorpus(corpusBody=CORPUSBODY):
    global corpus
    global ngram
    for item in corpusBody:
        corpusDict = {}
        corpusList = list()
        with open("newCorpus/" + item) as file:
            corpusList += file.readlines()
        for items in corpusList:
            if items not in corpusDict:
                corpusDict[items.replace('"', '').replace('\n', '').replace('[', '').replace(']', '')] = []
        for sentence in corpusDict.keys():
            linkedNodeList = n.LinkedList()
            splitSentence = sentence.split(' ')
            for i in range(1, len(splitSentence)+1):
                node = n.Node(splitSentence[i-1])
                linkedNodeList.insert(node)
                if wordLinkedListDict.get(splitSentence[i - 1]):
                    wordLinkedListDict[splitSentence[i - 1]].append(linkedNodeList)
                else:
                    tempList = list()
                    tempList.append(linkedNodeList)
                    wordLinkedListDict[splitSentence[i - 1]] = tempList


#              if '' in node.data:
#                  continue
                if (linkedNodeList) not in ngram:
                    ngram[linkedNodeList] = []
                    ngram[linkedNodeList].append(sentence.split(' ')[i-1])


def getResponse(message):
    out = ""
    outMinusIDK = ""
    processedMessage = processMessage(message)
    if int(len(processedMessage)) > 1:
        #thisManyLengths = how many responses babyBot should gives
        thisManyLengths = int(len(processedMessage) / 2)
    else:
        thisManyLengths = 1
    for i in range(thisManyLengths):
      linkedList = random.choice(processedMessage)
      if wordLinkedListDict.get(linkedList):
            #this shouldn't be random eventually. Eventually we want the bot to decide which context is best using tags
        outMinusIDK += random.choice(wordLinkedListDict[linkedList]).getLL()
        out += random.choice(wordLinkedListDict[linkedList]).getLL()
      else:
        out += " I do not know what {} means ".format(linkedList)

        #while True:
        #   if linkedList not in ngram.keys():
        #      break
        # third = random.choice(list(ngram[linkedList]))
        #if ngram.get(third):
        # out += ngram.get(third).getLL() + ' '


#        word_pair = (third[1], third)

    f = open("newCorpus/interactions.txt", "a")
    f.write(message + " " + "\n" + outMinusIDK + "\n")
    f.close()
    
    return out


def corpusInit(corpusBody=CORPUSBODY):
    populateCorpus(corpusBody)


def processMessage(message):
    messageList = list()
    messageList = message.split(" ")
    return messageList
