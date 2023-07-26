import math
import random

class Word:
    def __init__(self, pronunciation, meaning):
        self.pronunciation = pronunciation
        self.meaning = meaning

    def __str__(self):
        output = ""
        for s in self.pronunciation:
            output += str(s)
        return output

def generateSyllable(phonology):
    consonants = phonology[0]
    vowels = phonology[1]
    syl = []
    syl.append(consonants[math.floor(random.random() * len(consonants))])
    syl.append(vowels[math.floor(random.random() * len(vowels))])
    return syl

def generateWord(phonology, meaning):
    # between 1 and 4 syllables.
    # TODO: make this match a distribution of some kind.
    nSyllables = 1 + math.floor(random.random()*4)
    pronunciation = []
    for i in range(nSyllables):
        pronunciation += generateSyllable(phonology)
    # debug
    return Word(pronunciation, meaning)
