import random
import nodesr as n
from replit import db

CORPUSBODY = ("empty", "sample")
#"corpus.txt", "avatar.txt", "avatarScenes.txt", "interactions.txt", ("empty", "interactions.txt", "voaEnglish", "avatar", "got")

corpus = """"""
wordTagDict = {}
tagCorpusDict = {}
ngram = {}
corpusDict = {}
wordLinkedListDict = {}


def getCorpus():
    return corpus


def populateCorpus(corpusBody=CORPUSBODY):
  for item in corpusBody:
    corpusList = []
    with open ("newCorpus/" + item) as file:
      corpusList += file.readlines()
    for items in corpusList:
      wordList = items.split(" ")
      for i in range(0, len(wordList)):
        if db.get(wordList[i-1]):
          db[wordList[i-1]] = db[wordList[i-1]].append(wordList[i])
        else:
          thisList = []
          thisList.append(wordList[i])
          db[wordList[i-1]] = thisList
      

def getResponse(message):
  out = ""
  processedMessage = processMessage(message)
  if len(processedMessage) <= 2:
    counter = 2
  elif len(processedMessage) > 2 and len(processedMessage) <= 12:
    counter = int(len(processedMessage) / 2)
  elif len(processedMessage) > 12:
    counter = 12
  usedWords = []
  for i in range(random.randint(1,counter)):
    word = random.choice(processedMessage)
    if word in usedWords:
      pass
    else:
      if db.get(word) is None:
        out += "I do now know what {} means".format(word)
      else:
        out += random.choice(db[word]) + " "
      usedWords.append(word)
  return out

def processMessage(message):
  splitMessage = message.split(" ")
  if len(splitMessage) > 1:
    sendToDB(message)
    thisList = message.split(" ")
  else:
    thisList = [message]
  return thisList

#pass in a sentence, saves to DB as sequences
def sendToDB(sentence):
  wordList = sentence.split(" ")
  for i in range(0, len(wordList)+1):
    if db.get(wordList[i-1]):
      db[wordList[i-1]] = db[wordList[i-1]].append(wordList[i])
    else:
      thisList = []
      thisList.append(wordList[i])
      db[wordList[i-1]] = thisList

#taking out for a bit
def populaterCorpus(corpusBody=CORPUSBODY):
    global corpus
    global ngram
    for item in corpusBody:
        corpusDict = {}
        corpusList = []
        with open("newCorpus/" + item) as file:
            corpusList += file.readlines()
        for items in corpusList:
            if items not in corpusDict:
                corpusDict[items.replace('"', ' ').replace('\n', ' ').replace('[', ' ').replace(']', ' ')] = []
        for sentence in corpusDict.keys():
            linkedNodeList = n.LinkedList()
            splitSentence = sentence.split(" ")
            for i in range(1, len(splitSentence)+1):
                node = n.Node(splitSentence[i-1])
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
                    wordLinkedListDict[splitSentence[i-1]] = tempList


#              if '' in node.data:
#                  continue
     #           if (linkedNodeList) not in ngram:
    #              ngram[linkedNodeList] = []
   #               thisIsaList = []
  #                linkedNodeListSequence = linkedNodeList.printBackwards(thisIsaList)
 #                 for item in linkedNodeListSequence:
#                    ngram[item].append(splitSentence[i-1])

#taking out for a bit
def getrResponse(message):
    out = ""
    outMinusIDK = ""
    #processedMessage is a list of the message that was sent in a discord chat.
    processedMessage = processMessage(message)
    if int(len(processedMessage)) > 1:
        #thisManyLengths = how many responses babyBot should gives
        thisManyLengths = int(len(processedMessage) / 2)
    else:
        thisManyLengths = 1
    for i in range(thisManyLengths):
      linkedListWord = random.choice(processedMessage)
      if wordLinkedListDict.get(linkedListWord):
            #this shouldn't be random eventually. Eventually we want the bot to decide which context is best using tags
        outMinusIDK += random.choice(wordLinkedListDict[linkedListWord]).getLL()
        out += random.choice(wordLinkedListDict[linkedListWord]).getLL() + "??????"
      else:
        #with the changes I have made in the morning of 11.15 this will no longer be hit. ProcessMessage now saves the response to ngram list so this logic will never hit false
        out += " I do not know what {} means ".format(linkedListWord)

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


def processrMessage(message):
    messageList = list()
    messageList = message.split(" ")
    splitSentence = message.split(' ')
    for i in range(1, len(splitSentence)+1):
      linkedNodeList = n.LinkedList()
      node = n.Node(splitSentence[i-1])
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
            wordLinkedListDict[splitSentence[i-1]] = wordLinkedListDict.get(splitSentence[i-1]).append(item)
          else:
            wordLinkedListDict[splitSentence[i-1]] = tempList
            wordLinkedListDict[splitSentence[i-1]] = additionalTempList
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
