# Copyright (c) - 2015 Dagan Martinez

import sys
import lex.vocabulary
from nltk.stem.wordnet import WordNetLemmatizer

# Lists
punctuation = "\n\t\r`~!@#$%^&*()-_=+[]\\{}|;':\",./<>?"
JUNK_WORDS = [""]
DIGITS = list("1234567890")
COMMON_WORDS = lex.vocabulary.vocab


# Return a list of words from a list of texts
def get_words(texts, exclude=[]):
    # Clean up punctuation and all that jazz (HaCha!)
    # By converting the word list to a string
    print("\tCleaning up...")
    tempstring = " ".join(texts)
    if sys.version_info[0] == 3:
        tempstring = str(tempstring.encode('ascii', 'ignore')).lower()+" "  # Remove non-ASCII characters
    else:
        tempstring = tempstring.lower().decode('unicode_escape').encode('ascii', 'ignore')+" "  # Remove non-ASCII characters
    for i in punctuation:
        tempstring = tempstring.replace(i, " ")
    while tempstring != tempstring.replace("  ", " "):
        tempstring = tempstring.replace("  ", " ")

    # Remove duplicates and excluded items
    # Make list of words
    tempwords = list(set(tempstring.split(" ")))
    exclude = list(set(exclude))
    words = []
    print("\tRemoving excluded items...")
    for i in tempwords:
        if i.lower() not in exclude and not any(char.isdigit() for char in i):
            words.append(i)
    return words


def associate_words(words):
    lexicon = []
    while len(words) != 0:
        lexicon.append([words[0]])
        vl = WordNetLemmatizer().lemmatize(words[0].lower(), 'v')
        nl = WordNetLemmatizer().lemmatize(words[0].lower(), 'n')
        for i in words[1::]:
            vl2 = WordNetLemmatizer().lemmatize(i.lower(), 'v')
            nl2 = WordNetLemmatizer().lemmatize(i.lower(), 'n')
            if i == words[0] or vl2 == vl or nl2 == nl:
                lexicon[-1].append(i)
        for i in lexicon[-1]:
            words.remove(i)
        if vl not in lexicon[-1]:
            lexicon[-1].insert(0, vl)
        elif nl not in lexicon[-1]:
            if nl not in ["ass"]:
                lexicon[-1].insert(0, nl)
    return lexicon
