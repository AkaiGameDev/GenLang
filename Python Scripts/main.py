from soundSelection import *
from wordFormation import *
import json
from json import JSONEncoder

def testWordGen():
	# select sounds
	phonology = generatePhonologyNormal()

	selectedWords = []

	for i in range(10):
		selectedWords.append(generateWord(phonology, "nomeaning"))

	for w in selectedWords:
		print(w)

def testPhonologyGen():

	# select sounds
	phonology = generatePhonologyNormal()
	selectedConsonants = phonology[0]
	selectedVowels = phonology[1]

	# debugging
	print(f'selected {len(selectedConsonants)} consonants and {len(selectedVowels)} vowels:')
	for c in selectedConsonants:
		print(c)

	print("\n")

	for v in selectedVowels:
		print(v)

	for c in selectedConsonants:
		print(repr(c))
		print()

	for v in selectedVowels:
		print(repr(v))

if __name__ == '__main__':
	testPhonologyGen()