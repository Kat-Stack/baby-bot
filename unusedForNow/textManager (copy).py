import random
import nodes as n

CORPUSBODY = ("voaEnglish", "empty")
#"corpus.txt", "avatar.txt", "avatarScenes.txt", "interactions.txt",

corpus = """"""
wordTagDict = {}
tagCorpusDict = {}
ngram = {}
corpusList = list()
corpusDict = {}


def getCorpus():
    return corpus


def populateCorpus():
    global corpus
    global corpusList
    global ngram
    global corpusDict
    for item in CORPUSBODY:
        with open("newCorpus/" + item) as file:
            corpusList += file.readlines()
        for items in corpusList:
            if items not in corpusDict:
                corpusDict[items.lower().replace('"', '').replace(
                    "'", '').replace('\n', '').replace('[', '').replace(']', '')] = []
        for sentence in corpusDict.keys():
            for i in range(1, len(sentence.split(' '))):
                word_pair = (sentence.split(' ')[i - 1],
                             sentence.split(' ')[i - 0])
                if '' in word_pair:
                    continue
                if (word_pair) not in ngram:
                    ngram[word_pair] = []
                    ngram[word_pair].append(sentence.split(' ')[i])


def getResponse(message):
    word_pair = random.choice(list(ngram.keys()))
    out = word_pair[0] + ' ' + word_pair[1] + ' '

    while True:
        if word_pair not in ngram.keys():
            break
        third = random.choice(list(ngram[word_pair]))
        out += third + ' '
        word_pair = (word_pair[1], third)

    f = open("interactions.txt", "a")
    f.write(message + " " + "\n" + out + "\n")
    f.close()

    return out


def corpusInit():
    populateCorpus()
