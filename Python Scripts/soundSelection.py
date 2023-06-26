# This script is used to generate a phonology

# Current Version:
# The generator first decides how many consonants are going to be in this phonology
# Then it picks the most common consonants at random
# After the list of common consonants are exhausted, it picks the other consonants at random
# It decides either to use a 3 vowel system or a 5 vowel system
# These systems have predetermined vowels

# Here are some potential improvements for future versions:
# More vowel selection possibilities
# Including distinction for vowel quantity (how long it is held for)
# Phonemes can compose of multiple consonants
# Allophones

import numpy as np
import random
import math
import json
from json import JSONEncoder

class IpaSound:
	def __init__(self, descriptiveName, ipaChar, commonness="normal"):
		self.descriptiveName = descriptiveName
		self.ipaChar = ipaChar
		self.commonness = commonness
		self.manner = []
		self.place = []
		if "Vowel" in descriptiveName:
			self.type = "vowel"
		else:
			self.type = "consonant"
		if "Voiced" in descriptiveName:
			self.phonation = "voiced"
		else:
			self.phonation = "voiceless"
		if "Nasal" in descriptiveName:
			self.manner.append("nasal")
		if "Plosive" in descriptiveName or "Stop" in descriptiveName:
			self.manner.append("plosive")
		if "Sibilant" in descriptiveName or "Fricative" in descriptiveName:
			self.manner.append("fricative")
		if "Approximant" in descriptiveName:
			self.manner.append("approximant")
		if "Flap" in descriptiveName or "Tap" in descriptiveName:
			self.manner.append("flap")
		if "Trill" in descriptiveName:
			self.manner.append("trill")
		if "Click" in descriptiveName:
			self.manner.append("click")
		elif "Ejective" in descriptiveName:
			self.manner.append("ejective")
		elif "Implosive" in descriptiveName:
			self.manner.append("implosive")
		if "Lateral" in descriptiveName:
			self.lateral = True
		else:
			self.lateral = False
		if "Bilabial" in descriptiveName or "Labial" in descriptiveName:
			self.place.append("bilabial")
		if "Labiodental" in descriptiveName:
			self.place.append("labiodental")
		if "Linguolabial" in descriptiveName:
			self.place.append("linguolabial")
		if "Dental" in descriptiveName:
			self.place.append("dental")
		if "Alveolar" in descriptiveName:
			self.place.append("alveolar")
		if "Postalveolar" in descriptiveName or "Alveolopalatal":
			self.place.append("postalveolar")
		if "Retroflex" in descriptiveName:
			self.place.append("retroflex")
		if "Palatal" in descriptiveName:
			self.place.append("palatal")
		if "Velar" in descriptiveName:
			self.place.append("velar")
		if "Uvular" in descriptiveName:
			self.place.append("uvular")
		if "Epiglottal" in descriptiveName or "Pharyngeal" in descriptiveName:
			self.place.append("pharyngeal")
		if "Glottal" in descriptiveName:
			self.place.append("glottal")

		if self.type == "consonant" and (len(self.place) <= 0 or len(self.manner) <= 0):
			print(self.descriptiveName + " was not initialized correctly")
	def __str__(self):
		return self.ipaChar
	def __repr__(self):
		if self.type == "consonant":
			return f'This sound\'s IPA character is {self.ipaChar}, its descriptiveName is {self.descriptiveName}, \nits place of articulation is {self.place}, and its manner of articulation is {self.manner}'
		elif self.type == "vowel":
			return f'This sound\'s IPA character is {self.ipaChar}, its descriptiveName is {self.descriptiveName}'
		else:
			return f'This sound was imported incorrectly, its descriptiveName is {self.descriptiveName}'

def createAllIpaConsonants():
	# TODO: finish adding consonants
	# Create a list with the consonants from this page:
	# https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants
	# consonants described as "extremely rare" are excluded
	# consonants described as likely only existing in allophones are also excluded
	f = open("ipaConsonants.json", "r")
	dicts = json.load(f)
	output = []
	for d in dicts:
		output.append(IpaSound(d['descriptiveName'], d['ipaChar'], d['commonness']))
	return output

def create3VowelSystem():
	output = []
	output.append(IpaSound("CloseFrontUnroundedVowel", "i"))
	output.append(IpaSound("CloseBackRoundedVowel", "u"))
	output.append(IpaSound("OpenFrontUnroundedVowel", "a"))
	return output

def create5VowelSystem():
	output = []
	output.append(IpaSound("CloseFrontUnroundedVowel", "i"))
	output.append(IpaSound("CloseBackRoundedVowel", "u"))
	output.append(IpaSound("CloseMidFrontUnroundedVowel", "e"))
	output.append(IpaSound("CloseMidBackRoundedVowel", "o"))
	output.append(IpaSound("OpenFrontUnroundedVowel", "a"))
	return output

def selectConsonantsNormal(allConsonants=[]):
	# Follows distribution shown here: https://wals.info/chapter/1

	# populate allConsonants with all IPA consonants if no input
	if(len(allConsonants) <= 0):
		allConsonants = createAllIpaConsonants()
	
	# First decide how many consonants to pick
	# Decide which category we fall under, then pick a random number in that range
	# Every category other than large has a uniform distribution
	# Large has a exponential distribution to make extremely high inventories less likely
	category = math.floor(random.random() * 563)
	if (category < 89):	# Small (6 - 14)
		count = math.floor(random.random() * 9) + 6
	elif (category < (89 + 122)):	# Moderately Small (15 - 18)
		count = math.floor(random.random() * 4) + 15
	elif (category < (89 + 122 + 201)):	# Average (19 - 25)
		count = math.floor(random.random() * 7) + 19
	elif (category < (89 + 122 + 201 + 94)):	# Moderately Large (26 - 33)
		count = math.floor(random.random() * 8) + 26
	else:	# Large (34 - 122)
		count = math.floor(np.random.exponential(scale=0.2, size=1)[0] * 89) + 34
		if (count > len(allConsonants)):
			count = len(allConsonants)

	# Pick count # of consonants
	# TODO: make algorithm pick certain common consonants first
	output = []
	# Make a list of consonants with the common tag
	commonConsonants = []
	for s in allConsonants:
		if s.commonness == "common":
			commonConsonants.append(s)
	# pick common consonants first
	for i in range(count):
		if len(commonConsonants) > 0:
			pickIndex = math.floor(random.random() * len(commonConsonants))
			output.append(commonConsonants[pickIndex])
			allConsonants.remove(commonConsonants[pickIndex])
			commonConsonants.pop(pickIndex)
		else:
			pickIndex = math.floor(random.random() * len(allConsonants))
			output.append(allConsonants[pickIndex])
			allConsonants.pop(pickIndex)

	return output

def selectVowelsNormal():
	if random.random() < 0.5:
		selectedVowels = create3VowelSystem()
	else:
		selectedVowels = create5VowelSystem()
	return selectedVowels

def generatePhonologyNormal():
	selectedConsonants = selectConsonantsNormal()
	selectedVowels = selectVowelsNormal()
	return (selectedConsonants, selectedVowels)