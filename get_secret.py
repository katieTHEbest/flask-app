import random

nouns = []

with open("freqnoun.txt",'r',encoding = 'utf-8') as f:
    for line in f:
        text = line.split('\t')
        nouns.append(text[1])

def get_secret_word():
    word = random.choice(nouns)
    return word
