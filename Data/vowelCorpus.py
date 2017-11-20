import snowballstemmer
from TurkishStemmer import HasFrontness
from TurkishStemmer import HasRoundness
from TurkishStemmer import Vowels
import re
import sys

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
    if len(sys.argv) != 3:
        print("Error! Expected three command line arguments: scriptName fileToRead option")
        return
    f = open(sys.argv[1], 'r')
    option = int(sys.argv[2])
    turkishCorpus = f.read()
    wordList = turkishCorpus.split()
    stemmedWords = stemmer.stemWords(wordList)
    # print(wordList[0])
    # print(stemmedWords[0])
    count = 0
    ct = 0
    # options: 0 for normal run, 1 for consecutive bigrams, 2 for suffixing with bad harmony
    # in both arrays index 0 is perfect harmony, 1 is partial harmony, and 2
    # is breaking harmony
    wordHarm = [0, 0, 0]
    comp1 = []
    if option == 0:
        stemHarm = [0, 0, 0]
        for word in wordList:
            wordHarm[getHarmony(word)] += 1
        for stem in stemmedWords:
            stemHarm[getHarmony(stem)] += 1
        total1 = sum(wordHarm)
        total2 = sum(stemHarm)
        comp2 = []
        for val in wordHarm:
            comp1.append(str(100 * (val / total1)) + '%')
        for num in stemHarm:
            comp2.append(str(100 * (num / total2)) + '%')
        print('Filename: ' + sys.argv[1])
        print('Percent stems with perfect harmony: ' + comp2[0])
        print('Percent stems with partial harmony: ' + comp2[1])
        print('Percent stems failed harmony: ' + comp2[2])
        print('-------------------------------')
        print('Percent words with perfect harmony: ' + comp1[0])
        print('Percent words with partial harmony: ' + comp1[1])
        print('Percent words failed harmony: ' + comp1[2])
    if option == 1:
        for i in range (len(wordList) - 1):
            curr = wordList[i] + wordList[i + 1]
            wordHarm[getHarmony(curr)] += 1
        total = sum(wordHarm)
        for val in wordHarm:
            comp1.append(str(100 * (val / total)) + '%')
        print('Filename: ' + sys.argv[1])
        print('Percent bigrams with perfect harmony: ' + comp1[0])
        print('Percent bigrams with partial harmony: ' + comp1[1])
        print('Percent bigrams failed harmony: ' + comp1[2])
    if option == 2:
        added = []
        for i in range(len(wordList) - 1):
            s = stemmedWords[i]
            w = wordList[i]
            if getHarmony(s) == 2 and w not in added:
                # splitting breaks sometimes, this makes sure it doesnt
                try:
                    added.append(w)
                    w = (w.split(s))[1]
                    comp1.append((s, w))
                except IndexError:
                    continue
        print("Suffixing of words with failed harmony:")
        for pair in comp1:
            if pair[1] != '':
                print(pair[0] + '-' + pair[1])
    f.close()


# this code prints a few example words, stems, suffixes and their harmony check
# while ct < 10:
#     w = stemmedWords[count]
#     f = (wordList[count].split(w))[1]
#     print(wordList[count])
#     print(w)
#     print(wordList[count].split(w))
#     print(f)
#     count+=1
#     if (f != ''):
#         ct += 1
#         toPrint.append(w)
#         fix.append(f)
#     else:
#         continue
#
# for i in range(0, len(toPrint)):
#     print(toPrint[i])
#     print("Suffix: -" + fix[i])
#     checkHarmony(toPrint[i])
#     checkHarmonyAffix(fix[i])

if __name__ == "__main__":
    main()
