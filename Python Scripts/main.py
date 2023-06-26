from soundSelection import *
from wordFormation import *

def testWordGen():
	# select sounds
	selectedSounds = selectSounds()
	selectedConsonants = selectedSounds[0]
	selectedVowels = selectedSounds[1]

	selectedWords = []

	for i in range(10):
		selectedWords.append(generateWord(selectedConsonants, selectedVowels, "nomeaning"))

	for w in selectedWords:
		print(w)

def testSoundSelection():

	# select sounds
	selectedSounds = selectSounds()
	selectedConsonants = selectedSounds[0]
	selectedVowels = selectedSounds[1]

	# debugging
	print(f'selected {len(selectedConsonants)} consonants and {len(selectedVowels)} vowels:')
	for c in selectedConsonants:
		print(c)

	print("\n")

	for v in selectedVowels:
		print(v)

	for c in selectedConsonants:
		print(repr(c))

	print("\n")

	for v in selectedVowels:
		print(repr(v))

def selectSounds():
	selectedConsonants = selectConsonantsNormal()
	selectedVowels = selectVowelsNormal()
	return (selectedConsonants, selectedVowels)

if __name__ == '__main__':
	testWordGen()