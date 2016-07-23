from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import cmudict

import curses
from curses.ascii import isdigit

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


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
    corpus = getCorpus('Docs', '.*')

    haiku = findHaiku(corpus, 'comm_manifesto.txt')

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
    setInterval(runBot, 60*60*3)        #runs every 3 hours

# getCorpus('Docs', '.*')
# editDoc('Docs\mein_kampf.txt')