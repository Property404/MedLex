# Copyright (c) - 2015 Dagan Martinez

import sys
from stop_words import get_stop_words
import vocabulary

# Lists
punctuation = "\n\t\r`~!@#$%^&*()-_=+[]\\{}|;':\",./<>?"
JUNK_WORDS=get_stop_words('en')+[""]+list("abcdefghijklmnopqrstuvwxyz")
DIGITS=list("1234567890")
COMMON_WORDS=vocabulary.vocab

# Return a list of words from a list of texts
def getWords(texts, exclude=[]):
    # Clean up punctuation and all that jazz (HaCha!)
    # By converting the word list to a string
    print("\tCleaning up...")
    tempstring=" ".join(texts)
    if sys.version_info[0]==3:
        tempstring = str(tempstring.decode('unicode_escape').encode('ascii','ignore')).lower()+" " #Remove non-ASCII characters
    else:
        tempstring = tempstring.lower().decode('unicode_escape').encode('ascii','ignore')+" "#Remove non-ASCII characters
    for i in punctuation: tempstring = tempstring.replace(i, " ")
    while tempstring != tempstring.replace("  ", " "): tempstring = tempstring.replace("  ", " ")

    # Remove duplicates and excluded items
    # Make list of words
    tempwords=list(set(tempstring.split(" ")))
    exclude=list(set(exclude))
    words=[]
    print("\tRemoving excluded items...")
    for i in tempwords:
        if i.lower() not in exclude and not any(char.isdigit() for char in i):
            words.append(i)
    return words


# compare strings, return percentage
def str_comp_percentage(str1,str2):
    # Make sure str1 is the shortest
    if len(str1)>len(str2):
        temp=str1
        str1=str2
        str2=temp
    p=0
    # Compare strings
    for i in range(len(str1)):
        if str1[i].lower()==str2[i].lower():
            p+=1
        else:
            break
    return p/(len(str1)*1.0)


# Groups similiar words
def associateWords(words, per=.75):
    lexicon=[]
    a = 0
    while len(words)!=0:
        lexicon.append([words[0]])
        for i in words[1::]:
            if len(i)>3 and len(words[0])>3 and str_comp_percentage(words[0],i)>per:
                lexicon[-1].append(i)
        for i in lexicon[-1]:
            words.remove(i)
    return lexicon