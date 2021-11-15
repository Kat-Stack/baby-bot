from praw.models import MoreComments

# separates titles and URLs
def separator(listOfWords, urls='urls', titles='titles', addingCorpus = 'redditCorpus.txt'):
#    urlList = []
    titleList = []
    commentsList = []
    # had to have the encoding bit or it messed up at around entry 43 of the reddit scrape
#    title = open(titles, "w", encoding='utf-8')
#    url = open(urls, "w", encoding='utf-8')
    addToCorpus = open(addingCorpus, "a", encoding='utf-8')
    for x in listOfWords:
        titleList.append(x[0])
        for comment in x[len(x)-1]:
          if isinstance(comment, MoreComments):
            continue
          try:
            commentsList.append(comment.body)
          except:
            commentsList.append(comment)
#        urlList.append(x[1] + "\n")
    for item in commentsList:
      addToCorpus.write(item)
    for item in titleList:
      addToCorpus.write(item)
#    for item in urlList:
#        url.write(item)

def write_file(message, file):
    file.write(message.strip() + "\n")



# prints a file's text
def read_file(fileUrl):
    try:
        f = open(fileUrl, "r", encoding='utf-8')
        lines = []
        for x in f:
            lines.append(x.strip())
        return lines

    except IOError:
        print(fileUrl + " not accessible")

# Opens and returns a file
def open_file(fileUrl):
    try:
        f = open(fileUrl, "r")
        print(fileUrl + " has been opened")
        return f
    except IOError:
        print(fileUrl + " not accessible")


def main():
    print(read_file("data/urls"))


if __name__ == '__main__':
    main()
