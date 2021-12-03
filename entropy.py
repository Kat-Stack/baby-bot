import math
import random
import pickle
import os


#pull ngrams from pickle file and return
def readNgramsData(one, two, three, four, five):
    if one not in list(os.listdir("pickles/")):
        #these are example dictionaries
        oneEx = {}
        twoEx = {}
        threeEx = {}
        fourEx =  {}
        fiveEx = {}

        ngram1 = open(one, "wb")
        ngram2 = open(two, "wb")
        ngram3 = open(three, "wb")
        ngram4 = open(four, "wb")
        ngram5 = open(five, "wb")

        pickle.dump(oneEx, ngram1)
        pickle.dump(twoEx, ngram2)
        pickle.dump(threeEx, ngram3)
        pickle.dump(fourEx, ngram4)
        pickle.dump(fiveEx, ngram5)
        ngram1.close()
        ngram2.close()
        ngram3.close()
        ngram4.close()
        ngram5.close()
    return pickle.load(open(one,"rb")), pickle.load(open(two,"rb")), pickle.load(open(three,"rb")), pickle.load(open(four,"rb")), pickle.load(open(five,"rb"))

#adds words to the ngrams
def ngramManager(sentence, ngram1, ngram2, ngram3, ngram4, ngram5):
    splitSentence = sentence.split(" ")
    if len(splitSentence) <= 5:
        limit = len(splitSentence)
    else:
        limit = 5

    #IF there are enough words to make a "next" ngram, then the ngram is saved for all 5 ngrams
    for i in range(0, len(splitSentence)-limit):
        okNgrams = []
        if len(splitSentence) - limit - i > 0:
            if splitSentence[i] not in ngram1:
                ngram1[splitSentence[i]] = [0, {}]
            okNgrams.append(ngram1)
        if len(splitSentence) - limit - i > 1:
            if splitSentence[i] not in ngram2:
                tempDict = {
                    splitSentence[i]:
                        {
                            ngram1[splitSentence[i]]: splitSentence[i+1]
                        }
                }
                ngram2[tempDict] = [0, {}]
            okNgrams.append(ngram2)
        if len(splitSentence) - limit - i > 2:
            if splitSentence[i] not in ngram3:
                tempDict = {
                      ngram2[splitSentence[i]]: splitSentence[i+2]
                }
                ngram3[tempDict] = [0, {}]
            okNgrams.append(ngram3)
        if len(splitSentence) - limit - i > 3:
            if splitSentence[0] not in ngram4:
                tempDict = {
                    ngram3[splitSentence[0]]: splitSentence[3]
                }
                ngram4[tempDict] = [0, {}]
            okNgrams.append(ngram4)
        if len(splitSentence) - limit - i > 4:
            if splitSentence[0] not in ngram5:
                tempDict = {
                    ngram4[splitSentence[0]]: splitSentence[4]
                }
                ngram5[tempDict] = [0, {}]
            okNgrams.append(ngram5)

        for item in okNgrams:
            if item == ngram1:
#empty ngram    ngram1[splitSentence[0]] = [0, {}]
                ngram1[splitSentence[0]] += 1
                if splitSentence[0][splitSentence[1]] not in ngram1:
                    ngram1[splitSentence[0]][1][splitSentence[1]] = 0
                ngram1[splitSentence[0]][1][splitSentence[1]] += 1

            if item == ngram2:
                #for these we take the x ngrams and then the next x ngrams so words 0,1 for key and 2,3 for value
                #ngram2[[splitSentence[0], splitSentence[1]]][0] counter for totalCounter
                #[splitSentence[2], splitSentence[3]] next two words
                #ngram2[[splitSentence[0], splitSentence[1]]][1] dictionary for next ngram (key = ^, counter added to + created if not existing)
                #ngram2[splitSentence[0]][1][splitSentence[2], splitSentence[3]] adds next two words to dict
                ngram2[ngram1[splitSentence[0]]] += 1
                if splitSentence[0] not in ngram2:
                    if ngram1[splitSentence[0]] not in ngram2:
                        ngram2[splitSentence[0]][1][splitSentence[2]] = 0
                    ngram2[splitSentence[0]][1][splitSentence[2]] += 1

            if item == ngram3:
                ngram3[ngram2[splitSentence[0]]] += 1
                if ngram2[splitSentence[0]] not in ngram3:
                    ngram3[splitSentence[0]][1][splitSentence[3]] = 0
                ngram3[splitSentence[0]][1][splitSentence[3]] += 1

            if item == ngram4:
                ngram4[ngram2[splitSentence[0]]] += 1
                if ngram3[splitSentence[0]] not in ngram4:
                    ngram4[splitSentence[0]][1][splitSentence[4]] = 0
                ngram4[splitSentence[0]][1][splitSentence[4]] += 1

            if item == ngram5:
                ngram5[ngram4[splitSentence[0]]] += 1
                if ngram4[splitSentence[0]] not in ngram5:
                    ngram5[splitSentence[0]][1][splitSentence[5]] = 0
                ngram5[splitSentence[0]][1][splitSentence[5]] += 1

    return ngram1, ngram2, ngram3, ngram4, ngram5



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
