# NLP Assignment 1, Due 9/25/17
# Takes in a text file containing potential twitter handles and instagram names,
# then classifies them using RegExes based on length and character content.
# @authors Dan Brodkin, Kerim Celik

import re

    #open the file containing our data:
f = open("Assignment1_InputFile.txt")

    # set up regexes to classify each line's data based on its content
regex1 = re.compile("@[A-Za-z0-9_]{1,15}\s,\s(TI|I|N)$")
regex2 = re.compile(".*([Tt][Ww][Ii][Tt]{2}[Ee][Rr]).*")
regex3 = re.compile("@.*([Aa][Dd][Mm][Ii][Nn]).*")
regex4 = re.compile("@[A-Za-z0-9_.]{1,30}\s,\s(TI|I|N)$")
regex5 = re.compile(".*\sTI$")
regex6 = re.compile(".*\sI$")

    #set up the arrays and counters we'll be using to sort data
arr = []
types = []
i = 0
q = 0

    # loop through each line to apply the regexes
for lin in f:
    a = regex5.match(lin)
    b = regex6.match(lin)
    w = regex4.match(lin)
    x = regex1.match(lin)
    y = regex2.match(lin)
    z = regex3.match(lin)

    # sort the lines based on their content:
        # if they contain only legal characters, say they can be both
    if (a != None):
        types.append(0)
        # if twitter is ruled out, but insta is possible:
    elif (b != None):
        types.append(1)
        # if they fail at both:
    else:
        types.append(2)
    #try regex4; if it fails, this is neither
    #try regexes 1-3; if they work, then it's twitter
    if w == None:
        arr.append(2)
        #print("This can't be an instagram or a twitter handle.")
    elif (x != None) and (y == None) and (z == None):
        arr.append(0)
        #print("This can be either.")
    else:
        arr.append(1)
        #print("This can only be an instagram.")
    i += 1

both = 0
justInstas = 0
neither = 0

for n in range(len(types)):
    if types[n] == 0:                #adds to both total if both
        both += 1
    elif types[n] == 1:              #adds to insta total if it can only be that
        justInstas += 1
    elif types[n] == 2:               #adds to the 'neither total'
        neither += 1


#PRECISION = number instas identified in [arr] vs their identity in [types]
#RECALL = number instas identified in [arr] vs total number of instas in [types]

matchBoth = 0
matchInsta = 0
matchNeith = 0
countBoth = 0
countInsta = 0
countNeith = 0

for n in range(len(arr)):
    if (arr[n] == 0):
        countBoth += 1
        if (types[n] == arr[n]):
            matchBoth += 1
        elif (types[n] == 1):
            print("Confusion: handle " + str(n) + " was identified as Twitter and Instagram handle instead of just an Instagram handle!")
        else:
            print("Confusion: handle " + str(n) + " was identified as Twitter and Instagram handle instead of neither handle type!")
    elif (arr[n] == 1):
        countInsta += 1
        if (types[n] == arr[n]):
            matchInsta += 1
        elif (types[n] == 0):
            print("Confusion: handle " + str(n) + " was identified as just an Instagram handle instead of both a Twitter and Instagram handle!")
        else:
            print("Confusion: handle " + str(n) + " was identified as just an Instagram handle instead of neither handle type!")
    else:
        countNeith += 1
        if (types[n] == arr[n]):
            matchNeith += 1
        elif (types[n] == 1):
            print("Confusion: handle " + str(n) + " was identified as neither handle instead of just an Instagram handle!")
        else:
            print("Confusion: handle " + str(n) + " was identified as neither handle instead of both a Twitter and Instagram handle!")

prec1 = matchBoth/both
prec2 = matchInsta/justInstas
prec3 = matchNeith/neither
reca1 = countBoth/both
reca2 = countInsta/justInstas
reca3 = countNeith/neither
f1 = (2 * prec1 * reca1) / (prec1 + reca1)
f2 = (2 * prec2 * reca2) / (prec2 + reca2)
f3 = (2 * prec3 * reca3) / (prec3 + reca3)

print("Precision (both) = " + str(prec1 * 100) + "%")
print("Precision (just Instagram) = " + str(prec2 * 100) + "%")
print("Precision (neither) = " + str(prec3 * 100) + "%")
print("Recall (both) = " + str(reca1 * 100) + "%")
print("Recall (just Instagram) = " + str(reca2 * 100) + "%")
print("Recall (neither) = " + str(reca3 * 100) + "%")
print("F1 value (both) = " + str(f1))
print("F1 value (just Instagram) = " + str(f2))
print("F1 value (neither) = " + str(f3))
