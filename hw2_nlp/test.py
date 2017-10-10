from nltk.util import bigrams

sent = "Hi I am a test sentence to test your thing on."
print(list(bigrams(sent)))
