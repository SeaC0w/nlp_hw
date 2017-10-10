import nltk
import re
import math
from tabulate import tabulate
from nltk.util import ngrams
from nltk.util import bigrams
from nltk.util import trigrams
import sys

# creates a tokenizer to tokenize by sentence
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# comparison function used in sorting table of word occurences
def cmp_items(a, b):
    return a[1] - b[1]

# creates the three ngram dictionaries for a train/test split
def ngram_maker(sentences):
    unigram_dict = dict()
    bigram_dict = dict()
    trigram_dict = dict()
    # tokenize sentence by sentence, update dictionary accordingly
    for sent in sentences:
        unis = list(ngrams(nltk.word_tokenize(sent), 1))
        if (unis == []):
            continue
        for gram in unis:
            if gram not in unigram_dict.keys():
                unigram_dict[gram] = 1
            else:
                unigram_dict[gram] += 1

    # repeat for bigrams and trigrams
    for sent in sentences:
        bigs = list(bigrams(nltk.word_tokenize(sent)))
        if (bigs == []):
            continue
        if ('START', bigs[0][0]) not in bigram_dict.keys():
            bigram_dict[('START', bigs[0][0])] = 1
        else:
            bigram_dict[('START', bigs[0][0])] += 1
        for gram in bigs:
            if gram not in bigram_dict.keys():
                bigram_dict[gram] = 1
            else:
                bigram_dict[gram] += 1

    for sent in sentences:
        trigs = list(ngrams(nltk.word_tokenize(sent),3))
        if (trigs == []):
            continue
        # this line of code somehow causes the function to not read
        # the last sentence in the input file
        if ('START', 'START', trigs[0][0]) not in trigram_dict.keys():
            trigram_dict[('START', 'START', trigs[0][0])] = 1
        else:
            trigram_dict[('START', 'START', trigs[0][0])] += 1
        if ('START', trigs[0][0], trigs[0][1]) not in trigram_dict.keys():
            trigram_dict[('START', trigs[0][0], trigs[0][1])] = 1
        else:
            trigram_dict[('START', trigs[0][0], trigs[0][1])] += 1
        for gram in trigs:
            if gram not in trigram_dict.keys():
                trigram_dict[gram] = 1
            else:
                trigram_dict[gram] += 1

    # gets the total number of n-grams
    uni_total = 0
    bi_total = 0
    tri_total = 0
    for val in unigram_dict.values():
        uni_total += val
    for val in bigram_dict.values():
        bi_total += val
    for val in trigram_dict.values():
        tri_total += val

    # calculates the probability of each n-gram, stores back in dictionary
    for key in unigram_dict.keys():
        unigram_dict[key] = unigram_dict[key] / uni_total

    for key in bigram_dict.keys():
        bigram_dict[key] = bigram_dict[key] / bi_total

    for key in trigram_dict.keys():
        trigram_dict[key] = trigram_dict[key] / tri_total
    return ((unigram_dict, bigram_dict, trigram_dict), (uni_total, bi_total, tri_total))

# evaluates a sentence based on a specified train/test dictionary (model_dict)
# separate functions for each type of ngram
def eval_sent_uni(model_dict, sentence):
    prob = 1.0
    for gram in list(ngrams(nltk.word_tokenize(sentence), 1)):
        if gram not in model_dict.keys():
            prob *= 0.000001
        else:
            prob *= model_dict[gram]
    return prob

def eval_sent_bi(model_dict, sentence):
    prob = 1.0
    bigs = list(bigrams(nltk.word_tokenize(sentence)))
    if ('START', bigs[0][0]) not in model_dict.keys():
        prob *= 0.000001
    else:
        prob *= model_dict[('START', bigs[0][0])]
    for gram in bigs:
        if gram not in model_dict.keys():
            prob *= 0.000001
        else:
            prob *= model_dict[gram]
    return prob

def eval_sent_tri(model_dict, sentence):
    prob = 1.0
    trigs = list(ngrams(nltk.word_tokenize(sentence), 3))
    if ('START', 'START', trigs[0][0]) not in model_dict.keys():
        prob *= 0.000001
    else:
        prob *= model_dict[('START', 'START', trigs[0][0])]
    if ('START', trigs[0][0], trigs[0][1]) not in model_dict.keys():
        prob *= 0.000001
    else:
        prob *= model_dict[('START', trigs[0][0], trigs[0][1])]
    for gram in trigs:
        if gram not in model_dict.keys():
            prob *= 0.000001
        else:
            prob *= model_dict[gram]
    return prob

# argument d is the dictionary of probabilities created using a train set
# count is the total number of ngrams in the train set
def get_unigram_perplexity(sentences, d, count):
    perplex = 0
    # sums the MLEs for each sentence
    for sentence in sentences:
        perplex += eval_sent_uni(d, sentence)
    # exponentiates based on number of total n-grams in the passed dictionary
    perplex = perplex ** (-1 / count)
    return perplex

def get_bigram_perplexity(sentences, d, count):
    perplex = 0
    for sentence in sentences:
        perplex += eval_sent_bi(d, sentence)
    perplex = perplex ** (-1 / count)
    return perplex

def get_trigram_perplexity(sentences, d, count):
    perplex = 0
    for sentence in sentences:
        perplex += eval_sent_tri(d, sentence)
    perplex = perplex ** (-1 / count)
    return perplex

# data scrubbing function
def scrub(to_scrub):
    # scrub titles to prevent sentence interruptions
    to_scrub = re.sub('Dr.', 'Dr', to_scrub)
    to_scrub = re.sub('Mr.', 'Mr', to_scrub)
    to_scrub = re.sub('Mrs.', 'Mrs', to_scrub)
    to_scrub = re.sub('Ms.', 'Ms', to_scrub)
    # lower case all words to prevent distinction between
    # a word and its capitalized version
    to_scrub = to_scrub.lower()
    # switch all sentence ending punctuation to period for convenience
    to_scrub = re.sub('\?', '.', to_scrub)
    to_scrub = re.sub('!', '.', to_scrub)
    to_scrub = re.sub("'", " ", to_scrub)
    # remove other non-word punctuations
    to_scrub = re.sub('"', ' ', to_scrub)
    to_scrub = re.sub('\(', ' ', to_scrub)
    to_scrub = re.sub('\)', ' ', to_scrub)
    to_scrub = re.sub(',', ' ', to_scrub)
    to_scrub = re.sub(';', ' ', to_scrub)
    to_scrub = re.sub(':', ' ', to_scrub)
    to_scrub = re.sub('-', ' ', to_scrub)
    return to_scrub

def train_test_evaluate(train_test, inp):
    # opens the file to train and test on, scrubs it
    f = open(train_test, 'r')
    fil = f.read()
    fil = scrub(fil)

    # get sentence tokens and word tokens
    sent_tok = tokenizer.tokenize(fil)
    tokens2 = nltk.word_tokenize(fil)

    # tell the user the number of sentences and words in the file
    num_sent = len(sent_tok)
    num_word = 0
    tokens = []
    for wrd in tokens2:
        if wrd == '.':
            continue
        else:
            tokens.append(wrd)
            num_word += 1

    print('Number of sentences in file: ' + str(num_sent))
    print('Number of words in file: ' + str(num_word))
    print('\n')

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

    # sorts the table
    to_sort_table = [(y,x) for (x, y) in tabl]
    to_sort_table.sort()
    tabl = [(y,x) for (x, y) in to_sort_table]
    tabl.reverse()

    #prints the table using tabulate module
    print(tabulate(tabl, headers=['Word', 'Occurences']))

    # split the corpus into 90/10, 80/20, and 70/30 train/test splits
    sent90 = sent_tok[0:math.floor(0.9*len(sent_tok))]
    test10 = sent_tok[math.floor(0.9*len(sent_tok)):-1]
    sent80 = sent_tok[0:math.floor(0.8*len(sent_tok))]
    test20 = sent_tok[math.floor(0.8*len(sent_tok)):-1]
    sent70 = sent_tok[0:math.floor(0.7*len(sent_tok))]
    test30 = sent_tok[math.floor(0.7*len(sent_tok)):-1]

    # creates dictionaries to store the n-grams with their associated occurences
    # no need to create sentence end tag for bigram and trigram models as
    # the period of the sentences already acts as a sentence end tag
    tup = ngram_maker(sent90)
    unigram90 = tup[0][0]
    bigram90 = tup[0][1]
    trigram90 = tup[0][2]
    uni90count = tup[1][0]
    bi90count = tup[1][1]
    tri90count = tup[1][2]

    tup = ngram_maker(sent80)
    unigram80 = tup[0][0]
    bigram80 = tup[0][1]
    trigram80 = tup[0][2]
    uni80count = tup[1][0]
    bi80count = tup[1][1]
    tri80count = tup[1][2]

    tup = ngram_maker(sent70)
    unigram70 = tup[0][0]
    bigram70 = tup[0][1]
    trigram70 = tup[0][2]
    uni70count = tup[1][0]
    bi70count = tup[1][1]
    tri70count = tup[1][2]

    # get the overall preplexities for each train/test split for each type of ngram
    u90 = get_unigram_perplexity(test10, unigram90, uni90count)
    u80 = get_unigram_perplexity(test20, unigram80, uni80count)
    u70 = get_unigram_perplexity(test30, unigram70, uni70count)
    b90 = get_bigram_perplexity(test10, bigram90, bi90count)
    b80 = get_bigram_perplexity(test20, bigram80, bi80count)
    b70 = get_bigram_perplexity(test30, bigram70, bi70count)
    t90 = get_trigram_perplexity(test10, trigram90, tri90count)
    t80 = get_trigram_perplexity(test20, trigram80, tri80count)
    t70 = get_trigram_perplexity(test30, trigram70, tri70count)

    # create a table and print those perplexities
    tabl2 = [['Test10 unigram perplexity: ', u90], ['Test20 unigram perplexity: ', u80],
            ['Test30 unigram perplexity: ', u70], ['Test10 bigram perplexity: ', b90],
            ['Test20 bigram perplexity: ', b80], ['Test30 bigram perplexity: ', b70],
            ['Test10 trigram perplexity: ', t90], ['Test20 trigram perplexity: ', t80],
            ['Test30 trigram perplexity: ', t70]]
    print('\n')
    print(tabulate(tabl2, headers=['Test set and n-gram type', 'Perplexity Value']))

    # determine the best train/test split for each model
    uni_model = -1
    bi_model = -1
    tri_model = -1
    if (u90 <= u80) and (u90 <= u70):
        uni_model = 0
    elif (u80 <= u70):
        uni_model = 1
    else:
        uni_model = 2
    if (b90 <= b80) and (b90 <= b70):
        bi_model = 0
    elif (b80 <= b70):
        bi_model = 1
    else:
        bi_model = 2
    if (t90 <= t80) and (t90 <= t70):
        tri_model = 0
    elif (t80 <= t70):
        tri_model = 1
    else:
        tri_model = 2

    # open the file containing sentences to evaluate with the
    # trained and tested models
    f2 = open(inp, 'r')
    fil2 = f2.read()
    fil2 = scrub(fil2)

    # create a table to store the sentence MLEs
    tabl3 = []
    to_eval = tokenizer.tokenize(fil2)
    c = 0
    # calculate the MLE for unigram, bigram, and trigram models for each
    # sentence in the input file
    for sentence in to_eval:
        c += 1
        if uni_model == 0:
            entry = ["Sentence " + str(c) + " best unigram MLE:", eval_sent_uni(unigram90, sentence)]
        elif uni_model == 1:
            entry = ["Sentence " + str(c) + " best unigram MLE:", eval_sent_uni(unigram80, sentence)]
        else:
            entry = ["Sentence " + str(c) + " best unigram MLE:", eval_sent_uni(unigram70, sentence)]
        if bi_model == 0:
            entry1 = ["Sentence " + str(c) + " best bigram MLE:", eval_sent_bi(bigram90, sentence)]
        elif bi_model == 1:
            entry1 = ["Sentence " + str(c) + " best bigram MLE:", eval_sent_bi(bigram80, sentence)]
        else:
            entry1 = ["Sentence " + str(c) + " best bigram MLE:", eval_sent_bi(bigram70, sentence)]
        if tri_model == 0:
            entry2 = ["Sentence " + str(c) + " best trigram MLE:", eval_sent_tri(trigram90, sentence)]
        elif tri_model == 1:
            entry2 = ["Sentence " + str(c) + " best trigram MLE:", eval_sent_tri(trigram80, sentence)]
        else:
            entry2 = ["Sentence " + str(c) + " best trigram MLE:", eval_sent_tri(trigram70, sentence)]
        tabl3.append(entry)
        tabl3.append(entry1)
        tabl3.append(entry2)

    # print the sentence probabilities in a table
    print('\n')
    print(tabulate(tabl3, headers=['N-gram type', 'Sentence Probability']))

    # close the files
    f2.close
    f.close()

def main():
    # run instructions: "brodkind_celikk_hw2.py 'train/test file' 'input file'"
    if (len(sys.argv) != 3):
        print("Incorrect number of command line arguments: requires script name, train/test file name, and input file name")
    else:
        train_test_evaluate(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
