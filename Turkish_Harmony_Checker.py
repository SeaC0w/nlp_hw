---
Part 1: Load turkish text
#1) load words from file:
#2) run isTurkishWord() on each one

fopen = open("corpus", 'r', UTF-8)      #opens up our file
lexicon = []                            #creates list of Turkish words
for line in fopen:                      
    for word in line:
        word = stem(word)               #strip every morphological word into a stem
        if isTurkishWord(word) == True:     #if really a Turkish word:
            if word not in lexicon:         
                lexicon.append(word)        #add it to the lexicon
---
#Part 2: Check for Vowel Harmony

disharmonic = []                        #create list of disharmonic Turkish words
for token in lexicon:
    if not HasVowelHarmony(token):      #if a given token is disharmonic, 
        disharmonic.append(token)           #add it in to our list
---
#Part 3: Sort disharmonic tokens: some violate rounding, some violate frontness

badRounding = []            #creates lists of words which violate
badFronting = []            #rounding and backness harmony, respectively

for item in disharmonic:
    vowels = []             
    vowels = vowels(item)   #strip a word down to its vowels
    prev = ""
    cur = ""
    for vow in vowels:      #loop through and check vowel pairs
        prev = cur
        cur = vow
        if prev != "":
            if not HasFrontness(prev, cur):     #if there's no fronting harmony:
                badFronting.append(item)               #add to list of words without fronting harmony
            if not HasRoundness(prev, cur):     #if there's no rounding harmony:
                badRounding.append(item)                #add to list of words without backness harmony
                

Hard-coded version:
#2) A function to strip words down to vowels
# @parameter something to process
def Vowelfinder(readfile)       
    vowelDict = {}          #create a dictionary of word-vowelstring pairs
    for word in line:           #loop through words in file
        word = word.lower()     #lowercase the word
        holder = word           #create an unmodified form
        for ch in word:         #for each character in the word:
            if ch not in [a ı o u e i ö ü]:     #if not a vowel:
                word= word.replace(ch, "")          #get rid of it
        vowelDict[holder] = [word]              #add word, vowelstring pair to dictionary
    return vowelDict            #return the dictionary


#3) A function to check for backness harmony
# @parameter something to process
def FrontingChecker(readfile)
    #feed the function the text
    badFronting = []        #create list for words disharmonic in fronting

    for word in source                  #loop through words
            vowels = vowelDict[word]    #strip it down to vowels
            if vowels[0] in [a ı o u]:      #if the first vowel is BACK:
                for char in vowels:         #check if all others are BACK
                    if char not in [a ı o u]:       #if not:
                        badFronting.append(word)        #add to the list
            else:
                for char in vowels:     #if the first vowel is FRONT:
                    if ch not in [e i ö ü]:     #if any other vowel is NOT:
                        badFronting.append(word)    #add to the list
        return badFronting
    

#4) A function to check for roundness harmony
# @parameter something to process
def RoundingChecker(readfile)
    #feed the function the text
    badRounding = []        #create list for words disharmonic in rounding
    
        for word in source:             #loop through words
            vowels = vowelDict[word]    #strip down to vowels
            if vowels[0] in [o u ö ü]:  #if first vowel is ROUND:
                for char in vowels:         #check other vowels for ROUND
                    if ch not in [o u ö ü]:     #if any of them aren't:
                        badRounding.append(word)    #add to the list.
            else:
                for char in vowels:     #if first vowel is UNROUND:
                    if ch not in [a ı e i]:     #if any others are not:
                        badRounding.append(word)    #add to the list.