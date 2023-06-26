from soundSelection import IpaSound
import math
import random

class Word:
	def __init__(self, pronounciation, meaning):
		self.pronounciation = pronounciation
		self.meaning = meaning

	def __str__(self):
		output = ""
		for s in self.pronounciation:
			output += str(s)
		return output

def generateWord(consonants, vowels, meaning):
	pronounciation = []
	pronounciation.append(consonants[math.floor(random.random() * len(consonants))])
	pronounciation.append(vowels[math.floor(random.random() * len(vowels))])
	return Word(pronounciation, meaning)