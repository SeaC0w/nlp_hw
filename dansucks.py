import snowballstemmer
from TurkishStemmer import HasFrontness
from TurkishStemmer import HasRoundness
from TurkishStemmer import Vowels
import re
stemmer = snowballstemmer.stemmer('turkish')
# print(stemmer.stemWords("Genç çocuklar".split()))
# print(HasFrontness('o', 'u'))
# print(HasRoundness('o', 'u'))
# print("çocuklar".split('çoc')[0] + '-' + "çocuklar".split('çoc')[1])

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


f = open('scrubbed.txt')
turkishCorpus = f.read()
stemmedWords = stemmer.stemWords(turkishCorpus.split())
count = 0
toPrint = []
while count < 10:
    count+=1
    toPrint.append(stemmedWords[count])

# for word in toPrint:
#     word = re.sub('ı', '#', word)
#     word = re.sub('ş', '0', word)
#     word = re.sub('ç', '1', word)
#     word = re.sub('ö', '2', word)
#     word = re.sub('ğ', '3', word)
#     word = re.sub('ü', '4', word)
#     word = re.sub('Ğ', '5', word)
#     word = re.sub('Ü', '6', word)
#     word = re.sub('İ', '7', word)
#     word = re.sub('Ö', '8', word)
#     word = re.sub('Ş', '9', word)
#     word = re.sub('Ç', '@', word)

print(toPrint)
[checkHarmony(w) for w in toPrint]
