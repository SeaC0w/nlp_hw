import snowballstemmer
from TurkishStemmer import HasFrontness
from TurkishStemmer import HasRoundness
from TurkishStemmer import Vowels
import re

stemmer = snowballstemmer.stemmer('turkish')

def checkHarmony(word):
    vowels = Vowels(word)
    harm = []
    for i in range(len(vowels) - 1):
        ro = HasRoundness(vowels[i], vowels[i+1])
        fr = HasFrontness(vowels[i], vowels[i+1])
        if ro and fr:
            harm.append(0)
        elif ((ro and not fr) or (fr and not ro)):
            harm.append(1)
        else:
            harm.append(2)
    if (len(harm) == 0):
        check = 0
    else:
        check = max(harm)
    if check == 0:
        print(word + " has perfect vowel harmony")
    elif check == 1:
        print(word + " has partial vowel harmony")
    else:
        print(word + " breaks vowel harmony")

def checkHarmonyAffix(word):
    vowels = Vowels(word)
    harm = []
    for i in range(len(vowels) - 1):
        ro = HasRoundness(vowels[i], vowels[i+1])
        fr = HasFrontness(vowels[i], vowels[i+1])
        if ro and fr:
            harm.append(0)
        elif ((ro and not fr) or (fr and not ro)):
            harm.append(1)
        else:
            harm.append(2)
    if (len(harm) == 0):
        check = 0
    else:
        check = max(harm)
    if check == 0:
        print("The suffix " + word + " has perfect vowel harmony")
    elif check == 1:
        print("The suffix " + word + " has partial vowel harmony")
    else:
        print("The suffix " + word + " breaks vowel harmony")


f = open('scrubbed.txt')
turkishCorpus = f.read()
wordList = turkishCorpus.split()
stemmedWords = stemmer.stemWords(wordList)
count = 0
ct = 0
toPrint = []
fix = []
while ct < 10:
    w = stemmedWords[count]
    f = (wordList[count].split(w))[1]
    print(wordList[count])
    print(w)
    print(wordList[count].split(w))
    print(f)
    count+=1
    if (f != ''):
        ct += 1
        toPrint.append(w)
        fix.append(f)
    else:
        continue

for i in range(0, len(toPrint)):
    print(toPrint[i])
    print("Suffix: -" + fix[i])
    checkHarmony(toPrint[i])
    checkHarmonyAffix(fix[i])
