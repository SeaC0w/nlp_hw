import nltk
import re
import math
from tabulate import tabulate

# creates a tokenizer to tokenize by sentence
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

f = open("HW2_InputFile.txt", 'r')
fil = f.read()

# removes the period from title prefixes to prevent incorrect sentence splits
fil = re.sub('Dr.', 'Dr', fil)
fil = re.sub('Mr.', 'Mr', fil)
fil = re.sub('Mrs.', 'Mrs', fil)
fil = re.sub('Ms.', 'Ms', fil)

# get sentence tokens and word tokens
sent_tok = tokenizer.tokenize(fil)
tokens = nltk.word_tokenize(fil)

# tell the user the number of sentences and words in the file
num_sent = len(sent_tok)
num_word = len(tokens)
print('Number of sentences in file: ' + str(num_sent))
print('Number of words in file: ' + str(num_word))

# sort the words in file by number of occurences
# then print as a table
added = []
tabl = []
for item in tokens:
    if item not in added:
        tabl.append([item, 1])
        added.append(item)
    else:
        for row in tabl:
            if row[0] == item:
                row[1] += 1
tabl.sort()
print(tabulate(tabl, headers=['Word', 'Occurences']))

# split the corpus into 90/10, 80/20, and 70/30 train/test splits
sent90 = sent_tok[0:math.floor(0.9*len(sent_tok))]
test10 = sent_tok[math.floor(0.9*len(sent_tok)):-1]
sent80 = sent_tok[0:math.floor(0.8*len(sent_tok))]
test20 = sent_tok[math.floor(0.8*len(sent_tok)):-1]
sent70 = sent_tok[0:math.floor(0.7*len(sent_tok))]
test30 = sent_tok[math.floor(0.7*len(sent_tok)):-1]

# POS tag the words in the sentences, then append the tags to a single list for
# each train/test split
pos90 = []
pos80 = []
pos70 = []
for item in sent90:
    pairs = nltk.pos_tag(nltk.word_tokenize(item))
    for pair in pairs:
        pos90.append(pair[1])

for item in sent80:
    pairs = nltk.pos_tag(nltk.word_tokenize(item))
    for pair in pairs:
        pos80.append(pair[1])

for item in sent70:
    pairs = nltk.pos_tag(nltk.word_tokenize(item))
    for pair in pairs:
        pos70.append(pair[1])

# creates dictionaries to store the pos_tag n-grams with
# their associated occurences
# no need to create sentence end tag for bigram and trigram models as
# the period of the sentences already acts as a sentence end tag
unigram90 = dict()
bigram90 = dict()
trigram90 = dict()
for tag in pos90:
    if tag not in unigram90.keys():
        unigram90[tag] = 1
    else:
        unigram90[tag] += 1

prevtag = 'START'
for tag in pos90:
    if (prevtag, tag) not in bigram90.keys():
        bigram90[(prevtag, tag)] = 1
    else:
        bigram90[(prevtag, tag)] += 1
    prevtag = tag

preprevtag = 'START'
prevtag = 'START'
for tag in pos90:
    if (preprevtag, prevtag, tag) not in trigram90.keys():
        trigram90[(preprevtag, prevtag, tag)] = 1
    else:
        trigram90[(preprevtag, prevtag, tag)] += 1
    preprevtag = prevtag
    prevtag = tag

# gets the total number of n-grams for 90/10 split
uni90total = 0
bi90total = 0
tri90total = 0
for val in unigram90.values():
    uni90total += val
for val in bigram90.values():
    bi90total += val
for val in trigram90.values():
    tri90total += val

# calculates the probability of each n-gram for 90/10 split
for key in unigram90.keys():
    unigram90[key] = unigram90[key] / uni90total

for key in bigram90.keys():
    bigram90[key] = bigram90[key] / bi90total

for key in trigram90.keys():
    trigram90[key] = trigram90[key] / tri90total

# repeat above process for other train/test split ratios
# 80/20 train test split probability calculations
unigram80 = dict()
bigram80 = dict()
trigram80 = dict()
for tag in pos80:
    if tag not in unigram80.keys():
        unigram80[tag] = 1
    else:
        unigram80[tag] += 1

prevtag = 'START'
for tag in pos80:
    if (prevtag, tag) not in bigram80.keys():
        bigram80[(prevtag, tag)] = 1
    else:
        bigram80[(prevtag, tag)] += 1
    prevtag = tag

preprevtag = 'START'
prevtag = 'START'
for tag in pos80:
    if (preprevtag, prevtag, tag) not in trigram80.keys():
        trigram80[(preprevtag, prevtag, tag)] = 1
    else:
        trigram80[(preprevtag, prevtag, tag)] += 1
    preprevtag = prevtag
    prevtag = tag

# gets the total number of n-grams for 80/20 split
uni80total = 0
bi80total = 0
tri80total = 0
for val in unigram80.values():
    uni80total += val
for val in bigram80.values():
    bi80total += val
for val in trigram80.values():
    tri80total += val

# calculates the probability of each n-gram for 80/20 split
for key in unigram80.keys():
    unigram80[key] = unigram80[key] / uni80total

for key in bigram80.keys():
    bigram80[key] = bigram80[key] / bi80total

for key in trigram80.keys():
    trigram80[key] = trigram80[key] / tri80total

# 70/30 train test split probability calculations
unigram70 = dict()
bigram70 = dict()
trigram70 = dict()
for tag in pos70:
    if tag not in unigram70.keys():
        unigram70[tag] = 1
    else:
        unigram70[tag] += 1

prevtag = 'START'
for tag in pos70:
    if (prevtag, tag) not in bigram70.keys():
        bigram70[(prevtag, tag)] = 1
    else:
        bigram70[(prevtag, tag)] += 1
    prevtag = tag

preprevtag = 'START'
prevtag = 'START'
for tag in pos70:
    if (preprevtag, prevtag, tag) not in trigram70.keys():
        trigram70[(preprevtag, prevtag, tag)] = 1
    else:
        trigram70[(preprevtag, prevtag, tag)] += 1
    preprevtag = prevtag
    prevtag = tag

# gets the total number of n-grams for 70/30 split
uni70total = 0
bi70total = 0
tri70total = 0
for val in unigram70.values():
    uni70total += val
for val in bigram70.values():
    bi70total += val
for val in trigram70.values():
    tri70total += val

# calculates the probability of each n-gram for 70/30 split
for key in unigram70.keys():
    unigram70[key] = unigram70[key] / uni70total

for key in bigram70.keys():
    bigram70[key] = bigram70[key] / bi70total

for key in trigram70.keys():
    trigram70[key] = trigram70[key] / tri70total

# do the stuff on test sets


# close the file
f.close()
