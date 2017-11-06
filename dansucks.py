import snowballstemmer
# from TurkishStemmer import TurkishStemmer
stemmer = snowballstemmer.stemmer('turkish')
print(stemmer.stemWords("Genç çocuklar".split()))
print("çocuklar".split('çoc')[0] + '-' + "çocuklar".split('çoc')[1])
