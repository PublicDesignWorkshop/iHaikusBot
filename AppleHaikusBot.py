from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import cmudict

import curses
from curses.ascii import isdigit

import csv
import datetime

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

name = "iHaikus"

def getFollowers():
    """
    Gets details about followers of the bot
    """

    names = []                  #Name of follower
    usernames = []              #Username of follower
    ids = []                    #User id of follower
    locations = []              #Location of follower(as listed on their profile)
    follower_count = []         #How many followers the follower has
    time_stamp = []             #Date recorded

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")


    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    follower_count.append("# of their Followers")
    time_stamp.append("Time Stamp")

    next_cursor = -1

    #Get follower list (200)
    while(next_cursor):
        get_followers = twitter.get_followers_list(screen_name=name,count=200,cursor=next_cursor)
        for follower in get_followers["users"]:
            try:
                print(follower["name"].encode("utf-8").decode("utf-8"))
                names.append(follower["name"].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't Print")
            usernames.append(follower["screen_name"].encode("utf-8").decode("utf-8"))
            ids.append(follower["id_str"])

            try:
                print(follower["location"].encode("utf-8").decode("utf-8"))
                locations.append(follower["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't Print")

            follower_count.append(follower["followers_count"])
            time_stamp.append(datestamp)
            next_cursor = get_followers["next_cursor"]

    open_csv = open("followers.csv","r",newline='')                         #Read what has already been recorded in the followers file
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))

    rows = zip(names,usernames,ids,locations,follower_count,time_stamp)     #Combine lists

    oldFollowerIDs = []                                                     #Store followers that have already been recorded in the past

    oldFollowers_csv = csv.reader(open_csv)

    for row in oldFollowers_csv:
            oldFollowerIDs.append(row[2])

    open_csv.close()

    open_csv = open("followers.csv","a", newline='')        #Append new followers to the followers file
    followers_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[2] in oldFollowerIDs):                  #if the ID isn't already in the follower list
            followers_csv.writerow(row)

    open_csv.close()

def getMentionsRetweets():
    """
    Gets details of mentions/retweets of the user
    """

    names = []                  #Name of user who retweeted/mentioned
    usernames = []              #Their username
    ids = []                    #Their user id
    locations = []              #Their location (as listed on their profile)
    tweetIDs = []               #ID of the retweet/mention
    tweets = []                 #The retweet/mention text
    time_stamp = []             #Date the retweet/mention was created

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    tweetIDs.append("Tweet ID")
    tweets.append("Tweet Text")
    time_stamp.append("Time Stamp")

    #Get mentions (200)
    mentions_timeline = twitter.get_mentions_timeline(screen_name=name,count=200)
    for mention in mentions_timeline:
        try:
            print(mention['user']['name'].encode("utf-8").decode("utf-8"))
            names.append(mention['user']['name'].encode("utf-8").decode("utf-8"))
        except:
            names.append("Can't print")
        usernames.append(mention["user"]["screen_name"].encode("utf-8").decode("utf-8"))
        ids.append(mention["user"]["id_str"])
        try:
            print(mention["user"]["location"].encode("utf-8").decode("utf-8"))
            locations.append(mention["user"]["location"].encode("utf-8").decode("utf-8"))
        except:
            locations.append("Can't Print")
        tweetIDs.append(mention["id_str"])
        try:
            print(mention['text'].encode("utf-8").decode("utf-8"))
            tweets.append(mention['text'].encode("utf-8").decode("utf-8"))
        except:
            tweets.append("Can't Print")
        time_stamp.append(mention["created_at"].encode("utf-8").decode("utf-8"))

    #Get retweets (200)
    retweetedStatuses = twitter.retweeted_of_me(count = 100)                                    #Get tweets from the user that have recently been retweeted
    for retweetedStatus in retweetedStatuses:
        statusID = retweetedStatus["id_str"]
        retweets = twitter.get_retweets(id=statusID,count=100)                                  #Get the retweets of the tweet
        for retweet in retweets:
            try:
                print(retweet['user']['name'].encode("utf-8").decode("utf-8"))
                names.append(retweet['user']['name'].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't print")
            
            usernames.append(retweet["user"]["screen_name"].encode("utf-8").decode("utf-8"))

            ids.append(retweet["user"]["id_str"])

            try:
                print(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
                locations.append(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't print")
            
            tweetIDs.append(retweet["id_str"])
            
            try:
                print(retweet['text'].encode("utf-8").decode("utf-8"))
                tweets.append(retweet['text'].encode("utf-8").decode("utf-8"))
            except:
                tweets.append("Can't print")
            
            time_stamp.append(retweet["created_at"].encode("utf-8").decode("utf-8"))


    open_csv = open("mentions_retweets.csv","r",newline='')
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))
    # print(len(names))
    rows = zip(names,usernames,ids,locations,tweetIDs, tweets,time_stamp)

    oldMentionsIDs = []                             #Record mentions/retweets that have already been recorded before

    oldMentions_csv = csv.reader(open_csv)

    for row in oldMentions_csv:
            oldMentionsIDs.append(row[4])

    open_csv.close()

    open_csv = open("mentions_retweets.csv","a", newline='') #Append new mentions/retweets to the list
    mentions_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[4] in oldMentionsIDs):          #if the ID isn't already in the mentions list
            # print(row)
            mentions_csv.writerow(row)

    open_csv.close()

def tweet(tweet):
    """
    Tweets a string
    """
    twitter.update_status(status = tweet);


def getCorpus(fileLocation, fileids):
    """
    Takes in a location of files and  list of fileids and turns
    those files into corpus
    """
    docs = PlaintextCorpusReader(fileLocation, fileids)

    return docs



d = cmudict.dict()

def countSyllables(word):
    """
    Returns the amount of syllables in a word
    """
    try:
        return max([len([y for y in x if isdigit(y[-1])]) for x in d[word.lower()]])
    except:
        return None

def editDoc(docName):
    """
    Removes newlines from a txt file (so that sents() can take out the sentences correctly)
    """
    doc = open(docName, 'r')
    docList = doc.readlines()
    doc.close()

    newLines = []
    for line in docList:
        newLines.append(line.replace('\n', ''))

    doc = open(docName,'w')
    for line in newLines:
        doc.write(line)
    doc.close()


def checkIfHaiku(sentence):
    """
    Checks if the given sentence begins with a haiku
    """

    try:
        print(sentence)
    except:
        print("Can't print!")
    haiku = []      #will store the haiku
    wordIndex = 0


    #Find first line
    print("checking for first line!")
    syllableCount = 0
    
    while syllableCount < 5:                            #Keep checking words until you hit 5 syllables
        word = sentence[wordIndex].strip("1234567890")  #If the word has numbers, just give up
        if word == "":                                  #Because countSyllables() can't count syllables in numbers
            print("Has numbers")
            return None
        word = sentence[wordIndex].strip(".,'!?()[]-_:;\"1234567890")   #Take out punctuation just in case
        if word != "":
            wordSyllables = countSyllables(word)        #Get number of syllables of current word
            if wordSyllables == None:
                return None
            if syllableCount + wordSyllables <= 5:      #If it doesn't go over the syllable count
                syllableCount += wordSyllables
                if(word == "s" and haiku[-1] == "'"):   #If there's an "'s",
                    syllableCount = syllableCount - 1   #Don't count it as another syllable
                haiku.append(sentence[wordIndex])       #Add the word to the haiku
                wordIndex += 1
                if wordIndex >= len(sentence):          #If you reach the end of the sentence
                    print("Not a haiku!")
                    return None                         #give up
            else:                                       #The word takes the line over 5 syllables
                print("Not a haiku!")
                return None                             #Give up. It's not a haiku
        else:
            haiku.append(sentence[wordIndex])           #If the 'word' is just a punctuation mark
            wordIndex += 1                              #Just add it to the haiku
            if wordIndex >= len(sentence):              #If you reach end of sentence, give up
                print("Not a haiku!")
                return None

    haiku.append("\n")

    if wordIndex >= len(sentence):                      #If you're at the end of the sentence
        print("Not a haiku!")
        return None                                     #give up

    #Find second Line
    print("checking for second line!")
    syllableCount = 0
    
    while syllableCount < 7:                            #Keep checking words until you hit 7 syllables
        word = sentence[wordIndex].strip("1234567890")  #If the word has numbers, just give up
        if word == "":                                  #Because countSyllables() can't count syllables in numbers
            return None
        word = sentence[wordIndex].strip(".,'!?()[]-_:;\"1234567890")   #Take out punctuation just in case
        if word != "":
            wordSyllables = countSyllables(word)        #Get number of syllables of current word
            if wordSyllables == None:
                return None
            if syllableCount + wordSyllables <= 7:      #If it doesn't go over the syllable count
                syllableCount += wordSyllables
                if(word == "s" and haiku[-1] == "'"):   #If there's an "'s",
                    syllableCount = syllableCount - 1   #Don't count it as another syllable
                haiku.append(sentence[wordIndex])       #Add the word to the haiku
                wordIndex += 1
                if wordIndex >= len(sentence):          #If you reach the end of the sentence
                    print("Not a haiku!")
                    return None                         #give up
            else:                                       #The word takes the line over 5 syllables
                print("Not a haiku!")
                return None                             #Give up. It's not a haiku
        else:
            haiku.append(sentence[wordIndex])           #If the 'word' is just a punctuation mark
            wordIndex += 1                              #Just add it to the haiku
            if wordIndex >= len(sentence):              #If you reach end of sentence, give up
                print("Not a haiku!")
                return None

    haiku.append("\n")

    if wordIndex >= len(sentence):                      #If you're at the end of the sentence
        print("Not a haiku!")
        return None                                     #give up

    

    #Find third Line
    print("checking for third line!")
    syllableCount = 0
    
    while syllableCount < 5:                            #Keep checking words until you hit 5 syllables
        word = sentence[wordIndex].strip("1234567890")  #If the word has numbers, just give up
        if word == "":                                  #Because countSyllables() can't count syllables in numbers
            return None
        word = sentence[wordIndex].strip(".,'!?()[]-_:;><\"1234567890") #Take out punctuation just in case
        if word != "":
            wordSyllables = countSyllables(word)        #Get number of syllables of current word
            if wordSyllables == None:
                return None
            if syllableCount + wordSyllables <= 5:      #If it doesn't go over the syllable count
                syllableCount += wordSyllables
                if(word == "s" and haiku[-1] == "'"):   #If there's an "'s",
                    syllableCount = syllableCount - 1   #Don't count it as another syllable
                haiku.append(sentence[wordIndex])       #Add the word to the haiku
                wordIndex += 1
                if wordIndex >= len(sentence):          #If you reach the end of the sentence
                    print("Not a haiku!")
                    return None                         #give up
            else:                                       #The word takes the line over 5 syllables
                print("Not a haiku!")
                return None                             #Give up. It's not a haiku
        else:
            haiku.append(sentence[wordIndex])           #If the 'word' is just a punctuation mark
            wordIndex += 1                              #Just add it to the haiku
            if wordIndex >= len(sentence):              #If you reach end of sentence, give up
                print("Not a haiku!")
                return None

    badEnds = ["the", "a", "were", "of", "is", "are", "and", "my", "their"]             #bad words to end a haiku on (not a complete thought)

    if haiku[-1] in badEnds:                            #If haiku ends badly
        print("Haiku ends badly!")                      #don't return it
        return None

    return haiku

def findHaiku(corpus, docName):
    """
    Finds a random haiku in a document
    """
    sentences = corpus.sents(docName)                               #Get a list of sentences
    haiku = None

    

    while(haiku == None):                                           #Keep trying to find a haiku til you've found one
        sentence = sentences[randint(0, len(sentences)-1)]          #Get a random sentence from the list
        # print(sentence)
        haiku = checkIfHaiku(sentence)                              #Check if it starts with a haiku

        while(haiku == None and ("," in sentence or ";" in sentence)):  #If it doesn't start with a haiku, but it has commas or semicolons in it
            try:
                commaIndex = sentence.index(",")                        #Check if there are haikus in it starting after the commas
            except:
                commaIndex = None

            try:
                semiColIndex = sentence.index(";")                      #or after the semicolons
            except:
                semiColIndex = None

            puncIndex = -1
            if commaIndex == None:
                puncIndex = semiColIndex
            elif semiColIndex == None:
                puncIndex = commaIndex
            else:
                puncIndex = min(commaIndex, semiColIndex)
            sentence = sentence[puncIndex + 1:]
            haiku = checkIfHaiku(sentence)

    

    formatHaiku = ""

    index = 0

    for word in haiku:                                              #Format the haiku
        if word in ".,'!?-\":;" or word == "\n":
            if formatHaiku[-1:] == "\n":
                formatHaiku = formatHaiku[:-1] + word + "\n"
            else:
                formatHaiku = formatHaiku + word
        elif formatHaiku[-1:] == "-":
            formatHaiku = formatHaiku + word
        elif formatHaiku[-1:] == "\n":
            if word == word.upper():
                formatHaiku = formatHaiku + word
            else:
                formatHaiku = formatHaiku + word.capitalize()
        elif formatHaiku[-1:] == "'" and word == "s":
            formatHaiku = formatHaiku + word
        elif index == 0:
            if word == word.upper():
                formatHaiku = formatHaiku + word
            else:
                formatHaiku = formatHaiku + word.capitalize()
        else:
            formatHaiku = formatHaiku + " " + word
        index += 1

    print(formatHaiku)
    return formatHaiku

def runBot():
    try:
        getFollowers()
    except:
        print("Couldn't get Followers")

    try:        
        getMentionsRetweets()
    except:
        print("Couldn't get Mentions/Retweets")

    corpus = getCorpus('Docs', '.*')

    haiku = findHaiku(corpus, 'terms_and_conditions.txt')

    try:
        tweet(haiku)
        print("I just tweeted!")
    except:
        print("ran into a problem tweeting!")




def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60*6)        #runs every 6 hours

# getCorpus('Docs', '.*')
# editDoc('Docs\mein_kampf.txt')