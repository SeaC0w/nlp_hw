from TurkishStemmer import HasFrontness
from TurkishStemmer import HasRoundness
from TurkishStemmer import Vowels
import re
import sys

def getHarmony(word):
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
    return check

def main():
    if len(sys.argv) != 2:
        print("Error! Expected two command line arguments: scriptName fileToRead")
        return
    f = open(sys.argv[1], 'r')
    turkishCorpus = f.read()
    wordList = turkishCorpus.split()
    # print(wordList[0])
    count = 0
    ct = 0
    # in both arrays index 0 is perfect harmony, 1 is partial harmony, and 2
    # is breaking harmony
    wordHarm = [0, 0, 0]
    comp1 = []
    for word in wordList:
        wordHarm[getHarmony(word)] += 1
    total1 = sum(wordHarm)
    for val in wordHarm:
        comp1.append(str(100 * (val / total1)) + '%')
    print('Filename: ' + sys.argv[1])
    print('Percent words with perfect harmony: ' + comp1[0])
    print('Percent words with partial harmony: ' + comp1[1])
    print('Percent words failed harmony: ' + comp1[2])
    f.close()
