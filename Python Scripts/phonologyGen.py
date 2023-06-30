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
from tabulate import tabulate

class IpaSound:
	def __init__(self, descriptiveName, ipaChar):
		self.descriptiveName = descriptiveName
		self.ipaChar = ipaChar
	def __str__(self):
		return self.ipaChar
	def __repr__(self):
		return self.ipaChar


class IpaConsonant(IpaSound):
	def __init__(self, descriptiveName, ipaChar, commonness, phonation, manner, place, type):
		self.descriptiveName = descriptiveName
		self.ipaChar = ipaChar
		self.commonness = commonness
		self.phonation = phonation
		self.manner = manner
		self.place = place
		self.type = type
	def __repr__(self):
		return f'This sound\'s IPA character is {self.ipaChar}, its descriptiveName is {self.descriptiveName}, \nits place of articulation is {self.place}, and its manner of articulation is {self.manner}'

class IpaVowel(IpaSound):
	def __init__(self, descriptiveName, ipaChar, height, roundedness, backness):
		self.descriptiveName = descriptiveName
		self.ipaChar = ipaChar
		self.height = height
		self.roundedness = roundedness
		self.backness = backness

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
		output.append(IpaConsonant(d['descriptiveName'], d['ipaChar'], d['commonness'], d['phonation'], d['manner'], d['place'], d['type']))
	return output

def createAllIpaVowels():
	f = open("ipaVowels.json", "r")
	dicts = json.load(f)
	output = []
	for d in dicts:
		output.append(IpaVowel(d['descriptiveName'], d['ipaChar'], d['height'], d['roundedness'], d['backness']))
	return output

def create3VowelSystem():
	allvowels = createAllIpaVowels()
	output = []
	for v in allvowels:
		if v.ipaChar == "i" or v.ipaChar == "u" or v.ipaChar == "a":
			output.append(v)
	return output

def create5VowelSystem():
	allvowels = createAllIpaVowels()
	output = []
	for v in allvowels:
		if v.ipaChar == "i" or v.ipaChar == "u" or v.ipaChar == "e" or v.ipaChar == "o" or v.ipaChar == "a":
			output.append(v)
	return output

def create6VowelSystem():
	output = []


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

def displayPhonology(phonology):
	consonants = phonology[0]
	vowels = phonology[1]

	print("Pulmonic Consonants")
	print("In places where letters appear in pairs, the letter to the right respresents a voiced consonant, and the letter to the left represents an unvoiced consonant")
	print("In places where letters appear by themselves, the letter represents a voiced consonant")
	displayPulmonicConsonants(consonants)
	print("Non-pulmonic Consonants")
	displayNonpulmonicConsonants(consonants)

def displayPulmonicConsonants(consonants):
	pulmonicConsonants = [["", "Bilabial", "Labio-dental", "Linguo-labial", "Dental", "Alveolar", "Post-alveolar", "Retro-flex", "Palatal", "Velar", "Uvular", "Pharyngeal/epiglottal", "Glottal"]]
	pulmonicConsonants.append(["Nasal", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Plosive", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Sibilant fricative", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Non-sibilant fricative", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Approximant", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Tap/flap", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Trill", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Lateral fricative", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Lateral approximant", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])
	pulmonicConsonants.append(["Lateral tap/flap", ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]])

	pulmonicPlaceDict = {
		"bilabial": "Bilabial",
		"labiodental": "Labio-dental",
		"linguolabial": "Linguo-labial",
		"dental": "Dental",
		"alveolar": "Alveolar",
		"postalveolar": "Post-alveolar",
		"retroflex": "Retro-flex",
		"palatal": "Palatal",
		"velar": "Velar",
		"uvular": "Uvular",
		"pharyngeal": "Pharyngeal/epiglottal",
		"glottal": "Glottal"
	}

	pulmonicMannerDict = {
		"nasal": "Nasal",
		"plosive": "Plosive",
		"sibilant": "Sibilant fricative",
		"fricative": "Non-sibilant fricative",
		"approximant": "Approximant",
		"flap": "Tap/flap",
		"trill": "Trill",
		"lateralfricative": "Lateral fricative",
		"lateralapproximant": "Lateral approximant",
		"lateralflap": "Lateral tap/flap"
	}

	rowHeaders = []
	for r in pulmonicConsonants:
		rowHeaders.append(r[0])

	for c in consonants:
		if c.type == "pulmonic":
			column = pulmonicConsonants[0].index(pulmonicPlaceDict[c.place[0]])
			row = rowHeaders.index(pulmonicMannerDict[c.manner[0]])
			if c.phonation == "voiceless":
				pulmonicConsonants[row][column][0] = c.ipaChar
			elif c.phonation == "voiced":
				pulmonicConsonants[row][column][1] = c.ipaChar
			else:
				print(f'{c.descriptiveName} has a phonation that is not set correctly')

	trimTable(pulmonicConsonants)

	print(tabulate(pulmonicConsonants, tablefmt="simple_grid"))

def displayNonpulmonicConsonants(consonants):
	output = [["", "", "Bilabial", "Labio-dental", "Linguo-labial", "Dental", "Alveolar", "Post-alveolar", "Retro-flex", "Palatal", "Velar", "Uvular", "Pharyngeal/epiglottal", "Glottal"]]
	output.append(["Ejective", "Stop"])
	output.append(["", "Fricative"])
	output.append(["", "Lateral fricative"])
	output.append(["Click", "Tenuis"])
	output.append(["", "Voiced"])
	output.append(["", "Nasal"])
	output.append(["", "Tenuis lateral"])
	output.append(["", "Voiced lateral"])
	output.append(["", "Nasal lateral"])
	output.append(["Implosive", "Voiced"])
	output.append(["", "Voiceless"])

	placeDict = {
		"bilabial": "Bilabial",
		"labiodental": "Labio-dental",
		"linguolabial": "Linguo-labial",
		"dental": "Dental",
		"alveolar": "Alveolar",
		"postalveolar": "Post-alveolar",
		"retroflex": "Retro-flex",
		"palatal": "Palatal",
		"velar": "Velar",
		"uvular": "Uvular",
		"pharyngeal": "Pharyngeal/epiglottal",
		"glottal": "Glottal"
	}

	columnCount = len(output[0])
	for i, r in enumerate(output):
		while len(r) < columnCount:
			output[i].append("")

	# for c in consonants:
		# if c.type == "nonpulmonic":

	print(tabulate(output, tablefmt="simple_grid"))

def trimTable(table):
	for i, r in enumerate(table):
		for j, e in enumerate(r):
			if e == ['', '']:
				table[i][j] = ''
			elif type(e) is list and e[0] == '':
				table[i][j] = '   ' + e[1]
			elif type(e) is list and e[1] == '':
				table[i][j] = '   ' + e[0]
			elif type(e) is list:
				table[i][j] = e[0] + '  ' + e[1]
	return table