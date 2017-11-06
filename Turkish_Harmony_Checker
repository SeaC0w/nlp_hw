---
Part 1: Load turkish text
1) load words from file:
2) run isTurkishWord() on each one

fopen = open("corpus", 'r', UTF-8)      #opens up our file
lexicon = []                            #creates list of Turkish words
for line in fopen:                      
    for word in line:
        word = stem(word)               #strip every morphological word into a stem
        if isTurkishWord(word) == True:     #if really a Turkish word:
            if word not in lexicon:         
                lexicon.append(word)        #add it to the lexicon
---
Part 2: Check for Vowel Harmony

disharmonic = []                        #create list of disharmonic Turkish words
for token in lexicon:
    if not HasVowelHarmony(token):      #if a given token is disharmonic, 
        disharmonic.append(token)           #add it in to our list
---
Part 3: Sort disharmonic tokens: some violate rounding, some violate frontness

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
1) create stemmer by ourselves (holy fuck)   (SOLVED BY KERIM)
2) vowels function

vowelDict = {}
    ##get to reading the file
        for word in line:
            word = word.lower()
            holder = word
            for ch in word:
                if ch not in [a e i o u ü ö ı]:
                    word= word.replace(ch, "")
            vowelDict[holder] = [word] 

3) check backness harmony
4) check roundness harmony