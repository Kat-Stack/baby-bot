import nltk
import markovify
import os
import json
import random


# Needed functions:
# get nouns from sentence - (imports used) nltk
# create a kovify object from the message - (imports used) markovify
# load single kovify object from JSON file - (imports used) json + os
# save kovify object to JSON file  - (imports used) json + os
# combine existing dictionaries with new message input based on nouns - (imports used) markovify
# receive a message and process it through the response
from markovify.text import ParamError


class kovify_kr:

    def __init__(self, size, brain_directory):
        self.brain_index = {}
        self.ngram_size = size
        self.brain_directory = brain_directory

    # get the nouns from a text (adding enough periods to make it work if there arent enough). Returns list of nmaouns
    def get_nouns(self, message):
        lines = message
        is_noun = lambda pos: True if pos[:2] == 'NN' else False
        tokenized = nltk.word_tokenize(lines)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        return list(nouns)

    # receive a string and process it through the response
    def get_response(self, message, additional_tags=None):
        nouns_list = self.get_nouns(message)
        if additional_tags is not None:
            nouns_list = nouns_list.__add__(additional_tags)
        kovify_of_message = self.create_kovify(message)
        self.add_to_index(kovify_of_message, nouns_list)
        message_model = self.gen_new_brain(nouns_list)
        message_split = message.split(" ")
        try:
            attempt = message_model.make_sentence_with_start(message_split[-3])
        except KeyError:
            try:
                print("attempt failed on {}".format(message_split)[-3])
                attempt = message_model.make_sentence_with_start(random.choice(nouns_list), strict=False)
            except ParamError:
                print("attempt failed again on {}".format(message_split)[-3])
                attempt = message_model.make_sentence()
                if attempt is None:
                    attempt = "I tried to make a string but i failed. Maybe when i learn more words :pleading eyes:"
        except IndexError:
            try:
                print("index failed on {}".format(message_split)[-1])
                attempt = message_model.make_sentence_with_start(random.choice(nouns_list), strict=False)
            except ParamError:
                print("attempt failed again on {}".format(message_split)[-1])
                attempt = message_model.make_sentence()
                if attempt is None:
                    attempt = "I tried to make a string but i failed. Maybe when i learn more words :pleading eyes:"
        except ParamError:
            print("param failed again on {}".format(message_split)[-3])
            attempt = message_model.make_sentence()
        return attempt



    # create a kovify object from the message - (imports used) markovify
    def create_kovify(self, message):
        lines = message
        if len(lines.split(" ")) < self.ngram_size:
            lines += ". . . . ."
        kovify_model = markovify.Text(lines, state_size=self.ngram_size, well_formed=False, retain_original=False)
        return kovify_model

    # combine existing dictionaries with new message input based on nouns - (imports used) markovify
    def add_to_index(self, new_kovify, noun_list):
        for item in noun_list:
            if item in self.brain_index:
                self.brain_index[item] = markovify.combine([self.brain_index[item],new_kovify])
            else:
                self.brain_index[item] = new_kovify

    #gen a new model based on the nouns, return model
    def gen_new_brain(self, noun_list):
        new_model = markovify.Text(". . . . ", state_size=self.ngram_size)
        for item in noun_list:
            new_model = markovify.combine([new_model, self.brain_index[item]])
        print(new_model.make_sentence())
        return new_model

    # save kovify object to JSON file  - (imports used) json + os
    def save_whole_brain(self):
        for item in self.brain_index.keys():
            try:
                with open(str(self.brain_directory) + str(item) + ".json", "w", encoding='utf-8') as f:
                    json.dump(self.brain_index[item].to_json(), f)
            except Exception as e:
                print("issue dumping {}".format(item))

    # load kovify object from JSON file - (imports used) json + os
    def load_single_kovify(self, file_string):
        removed_json = file_string[len(self.brain_directory):].strip(".json")
        with open(file_string) as f:
            kovify_model = markovify.Text.from_json(json.load(f))
        self.brain_index[removed_json] = kovify_model

    #load entire brain index from folder filled with json file
    def load_entire_brain(self):
        for file in os.listdir(self.brain_directory):
            self.load_single_kovify(self.brain_directory+file)

    # devours the text from a text file
    def eatTextFiles(self,file, fileString = None):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()
            messageToLoad = ""
            counter = 0
            overall_count = 0
            for line in lines:
                if line != " ":
                    for finalSplit in line.replace("\n", ".").split("."):
                        messageToLoad += finalSplit + "."
                    messageToLoad += " "
                    counter += 1
                    if counter > 0:
                        print("line " + str(overall_count) + " " + self.get_response(messageToLoad, additional_tags=[fileString,])+"\n")
                        counter = 0
                        overall_count += 1
                        messageToLoad = ""

            print(self.get_response(messageToLoad, additional_tags=[fileString,])+"\n")

    # adds multiple text files to a corpus
    def addToCorpus(self,corpusTextFile):
        with open(corpusTextFile, encoding='utf-8') as f:
            for item in f:
                print("starting {}".format(item))
                index_of_slash = item.index("/")
                self.eatTextFiles(item.strip("\n"), fileString=item[index_of_slash+1:].strip(".txt\n"))
                print("finished {}".format(item))