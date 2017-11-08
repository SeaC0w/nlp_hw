import re
import sys

def scrub(fil, outName):
    f = open(fil, 'r')
    to_scrub = f.read()
    to_scrub = re.sub('Dr.', '', to_scrub)
    to_scrub = re.sub('/Noun', '', to_scrub)
    to_scrub = re.sub('/Undef', '', to_scrub)
    to_scrub = re.sub('/Adj', '', to_scrub)
    to_scrub = re.sub('/Verb', '', to_scrub)
    to_scrub = re.sub('/Adv', '', to_scrub)
    to_scrub = re.sub('/Det', '', to_scrub)
    to_scrub = re.sub('/Conj', '', to_scrub)
    to_scrub = re.sub('/Num', '', to_scrub)
    to_scrub = re.sub('/Postp', '', to_scrub)
    to_scrub = re.sub('/Pron', '', to_scrub)
    to_scrub = re.sub('/Punc', '', to_scrub)
    to_scrub = re.sub('/Ques', '', to_scrub)
    to_scrub = re.sub('0', '', to_scrub)
    to_scrub = re.sub('1', '', to_scrub)
    to_scrub = re.sub('2', '', to_scrub)
    to_scrub = re.sub('3', '', to_scrub)
    to_scrub = re.sub('4', '', to_scrub)
    to_scrub = re.sub('5', '', to_scrub)
    to_scrub = re.sub('6', '', to_scrub)
    to_scrub = re.sub('7', '', to_scrub)
    to_scrub = re.sub('8', '', to_scrub)
    to_scrub = re.sub('9', '', to_scrub)
    to_scrub = re.sub('\?', ' ', to_scrub)
    to_scrub = re.sub('!', ' ', to_scrub)
    to_scrub = re.sub("'", " ", to_scrub)
    to_scrub = re.sub('"', ' ', to_scrub)
    to_scrub = re.sub('\(', ' ', to_scrub)
    to_scrub = re.sub('\)', ' ', to_scrub)
    to_scrub = re.sub(',', ' ', to_scrub)
    to_scrub = re.sub(';', ' ', to_scrub)
    to_scrub = re.sub(':', ' ', to_scrub)
    to_scrub = re.sub('-', ' ', to_scrub)
    # lowercasing turkish messes the file up
    # to_scrub = to_scrub.lower()
    outfile = open(outName, 'w+')
    outfile.write(to_scrub)
    outfile.close()
    f.close()

def main():
    if len(sys.argv) != 3:
        print("Error! Expected three command line arguments: scriptName fileToRead outputFileName")
        return
    scrub(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
