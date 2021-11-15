import praw
import re
import time
import file_editor as fe
import sorter


sortBy = ['hot', 'new', 'controversial', 'top', 'gilded']


client_id = 'vika0p5YMk-VUg'
client_secret = 'S0MVD73hgvBq7bnvVAHwHzacmfq61Q'
user_agent = 'TopicScraper'
username = 'retest_bot'
password = 'This is my password'
default = 'subredit.txt'


def create_reddit_object():

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         username=username,
                         password=password)

    return reddit



#.hot
#.new
#.controversial
#.top
#.gilded


def remove_subred(subredToRemove):
    subred = []
    with open(default, "r+") as f:
        subreds = f.readlines()
        for item in subreds:
            if item.__eq__(subredToRemove + '\n') or item.__eq__(subredToRemove):
                pass
            elif item.__eq__('\n'):
                pass
            else:
                subred.append(item)
    with open(default, 'w') as f:
        for item in subred:
            f.write(item)


#add a subreddit to the list
def add_subred(subred):
    with open(default, "a") as f:
        f.write('\n' + subred)


#prints subreddits out
def read_subreds():
    with open(default) as f:
        for line in f:
            print(line.strip())


def menu(reddit):
    flag = True
    while flag:
        print("\nPick your choice!")
        print("1. Pull from defaults")
        print("2. Pull from a category")
        print("3. Subreddit functions")
        print("4. Sort Your Data")
        print("5. Exit")
        input1 = input()
        if input1 == "1":
            print("How many titles would you like to collect from each subreddit?")
            titleCount = int(input())
            subreditChooser(reddit, limits=titleCount)
            print("Completed the default data gathering")
        elif input1 == "2":
            print("Make a choice (0-4)" + sortBy.__str__())
            input2 = input()
            print("How many titles would you like to collect from each subreddit?")
            titleCount = int(input())
            if input2 == "0":
                subreditChooser(reddit, open(default), sortBy[0], titleCount)
            elif input2 == "1":
                subreditChooser(reddit, open(default), sortBy[1], titleCount)
            elif input2 == "2":
                subreditChooser(reddit, open(default), sortBy[2], titleCount)
            elif input2 == "3":
                subreditChooser(reddit, open(default), sortBy[3], titleCount)
            elif input2 == "4":
                subreditChooser(reddit, open(default), sortBy[4], titleCount)
            print("Completed the categorized data gathering")
        elif input1 == "3":
            print("What would you like to do?")
            print("1. Add a subreddit")
            print("2. Remove a subreddit from the list")
            print("3. View current subreddits")
            input2 = input()
            if input2.__eq__("1"):
                print("What subreddit would you like to add?")
                subAdd = input()
                add_subred(subAdd)
                print(subAdd + " added")
            elif input2.__eq__("2"):
                print("What subreddit would you like to remove?")
                read_subreds()
                subRem = input()
                remove_subred(subRem)
                print(subRem + " removed")
            elif input2.__eq__("3"):
                print("Current subreddits:")
                read_subreds()
                print("\nENTER to continue...")
                input()
            else:
                print("Invalid answer")
        elif input1 == "4":
            #input a list
            sorter.sorter(fe.read_file("./data/titles"))
        elif input1 == "5":
            flag = False
        else:
            print("Bad input.")


# grabs titles and urls from the chosen subreddits (stored in data/subredit)
def subreditChooser(reddit, subredit=open('subredit.txt'), category=sortBy[0], limits=10):
    listOfTitles = []
    for item in subredit:
        if not item.__eq__('\n') and not item.__eq__('') and not item.__eq__(' '):
            subred = reddit.subreddit(item.strip())
            print(subred)
            if category == sortBy[0]:
                post = subred.hot(limit=limits)
            elif category == sortBy[1]:
                post = subred.new(limit=limits)
            elif category == sortBy[2]:
                post = subred.controversial(limit=limits)
            elif category == sortBy[3]:
                post = subred.top(limit=limits)
            elif category == sortBy[4]:
                post = subred.gilded(limit=limits)
            #type(post)
            #x = next(post)
            #dir(x)

            # loop through hot posts and split title and url
            for i in post:
              try:
                tempList = [i.title, i.url, i.comments, i.comments.list()]
                listOfTitles.append(tempList)
              except AttributeError:
                tempList = [i.body]
                listOfTitles.append(tempList)


    fe.separator(listOfTitles)


def redditBotInit():
    reddit = create_reddit_object()
    print("Bot Active")
    menu(reddit)


def main():
  pass

if __name__ == '__main__':
    main()