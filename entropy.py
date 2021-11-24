import math
import random

#adds words to the ngrams
def ngramManager(sentence, dictionar):
    if len(sentence) > 3:
        for i in range(0, len(sentence.split(' ')) - 2):
            word_pair = (sentence.split(" ")[i], sentence.split(" ")[i + 1])
            if '' in word_pair:
                continue
            if word_pair not in dictionar:
                tempCount = 0
                dictionar[word_pair] = [tempCount, {}]
            addWords(dictionar, word_pair, sentence.split(' ')[i + 2])
        try:
            return word_pair
        except:
            word_pair = ("don't", " know")
            return word_pair
    word_pair = ("don't", "know")
    return word_pair


#adds words to the word pair next word dictionary (values)
def addWords(dictionar, word_pair, stringValue):
    dictionar[word_pair][0] += 1
    tempDict = dictionar[word_pair][1] #this is just for readability. we don't use this, we hard code it in
    if stringValue not in dictionar[word_pair][1]:
        dictionar[word_pair][1][stringValue] = 0
    dictionar[word_pair][1][stringValue] += 1


#calculates probabilities for next word. Returns a dictionary with all probabilities, the highest probability, and the lowest probability
def calculateProbabilities(wordPairDictionary, word):
    probabilityDict = {}
    total = wordPairDictionary[0]
    highestProbability = 0
    lowestProbability = 0
    lowestProbabilityItem = ""
    highestProbabilityItem = ""
    for items in wordPairDictionary[word][1]:
        probability = wordPairDictionary[word][1][items] / total
        if probability > highestProbability:
            highestProbabilityItem = items
        elif probability < lowestProbability:
            lowestProbabilityItem = items
        probabilityDict[items] = probability
    return probabilityDict, highestProbabilityItem, lowestProbabilityItem


#given a message and an ngrams dictionary, what is your response?
def getResponse(message, dictionar):
    word_pair = ngramManager(message, dictionar)
    out = word_pair[0] + ' ' + word_pair[1] + ' '
    while True:
        if word_pair not in dictionar.keys() or word_pair[1] == dictionar[word_pair] or word_pair[0] == dictionar[word_pair]:
            break
        if len(out) > 1000:
            break
        fullDict, highestItem, lowestItem = calculateProbabilities(dictionar, word_pair[1])
        third = dictionar[word_pair][1][lowestItem] # lowest = most confident
        out += third + ' '
        word_pair = (word_pair[1], third)