import snowballstemmer
from TurkishStemmer import HasFrontness
from TurkishStemmer import HasRoundness
from TurkishStemmer import Vowels
import sys
import re
stemmer = snowballstemmer.stemmer('turkish')

def checkHarmony(word):
    vowels = Vowels(word)
    harm = []
    for i in range(len(vowels) - 1):
        ro = HasRoundness(vowels[i], vowels[i+1])
        fr = HasFrontness(vowels[i], vowels[i+1])
        if (ro and fr):
            harm.append(0)
        elif ((ro and not fr) or (fr and not ro)):
            harm.append(1)
        else:
            harm.append(2)
    if (len(harm) == 0):
        # print('hey')
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
        if word == '':
            print("No suffix, therefore perfect vowel harmony")
            return
        print("The suffix " + word + " has perfect vowel harmony")
    elif check == 1:
        print("The suffix " + word + " has partial vowel harmony")
    else:
        print("The suffix " + word + " breaks vowel harmony")

def scrub(st):
    st = re.sub('ı', '#', st)
    st = re.sub('ş', '0', st)
    st = re.sub('ç', '1', st)
    st = re.sub('ö', '2', st)
    st = re.sub('ğ', '3', st)
    st = re.sub('ü', '4', st)
    st = re.sub('Ğ', '5', st)
    st = re.sub('Ü', '6', st)
    st = re.sub('İ', '7', st)
    st = re.sub('Ö', '8', st)
    st = re.sub('Ş', '9', st)
    st = re.sub('Ç', '@', st)
    return st

def main():
    word = sys.argv[1]
    # print(word)
    stem = stemmer.stemWord(word)
#    print(stem)
#    print(word.split(stem))
    suffix = (word.split(stem))[1]
    # suffix = scrub(suffix)
    print(stem + ' --- ' + suffix)
    checkHarmony(word)
    checkHarmony(stem)
    checkHarmonyAffix(suffix)

if __name__ == '__main__':
    main()
