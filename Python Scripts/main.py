from phonologyGen import *
from wordGen import *
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

def updateJsonFile():
	consonants = createAllIpaConsonants()
	output = []
	for c in consonants:
		output.append({
			"descriptiveName": c.descriptiveName,
			"ipaChar": c.ipaChar,
			"commonness": c.commonness,
			"phonation": c.phonation,
			"manner": c.manner,
			"place": c.place,
			"type": c.type
			})
	f = open("newIpaConsonants.json", "w")
	json.dump(output, f, indent=2)

if __name__ == '__main__':
	create3VowelSystem()
	create5VowelSystem()