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

class IpaSound:
	def __init__(self, descriptiveName, ipaChar, commonness="normal"):
		self.descriptiveName = descriptiveName
		self.ipaChar = ipaChar
		self.commonness = commonness
		self.manner = []
		self.place = []
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
		if "Postalveolar" in descriptiveName:
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
	def __str__(self):
		return self.ipaChar
	def __repr__(self):
		return f'This sound\'s IPA character is {self.ipaChar}, its descriptiveName is {self.descriptiveName}, \nits place of articulation is {self.place}, and its manner of articulation is {self.manner}\n'
		# return self.ipaChar

def createAllIpaConsonants():
	# TODO: finish adding consonants
	# Create a list with the consonants from this page:
	# https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants
	# consonants described as "extremely rare" are excluded
	# consonants described as likely only existing in allophones are also excluded
	output = []
	output.append(IpaSound("VoicelessBilabialNasal", "m̥"))
	output.append(IpaSound("VoicedBilabialNasal", "m", "common"))
	output.append(IpaSound("VoicedLabiodentalNasal", "ɱ"))
	output.append(IpaSound("VoicelessAlveolarNasal", "n̥"))
	output.append(IpaSound("VoicedAlveolarNasal", "n", "common"))
	output.append(IpaSound("VoicedRetroflexNasal", "ɳ"))
	output.append(IpaSound("VoicelessPalatalNasal", "ɲ̊"))
	output.append(IpaSound("VoicedPalatalNasal", "ɲ"))
	output.append(IpaSound("VoicelessVelarNasal", "ŋ̊"))
	output.append(IpaSound("VoicedVelarNasal", "ŋ"))
	output.append(IpaSound("VoicedUvularNasal", "ɴ"))
	output.append(IpaSound("VoicelessBilabialPlosive", "p", "common"))
	output.append(IpaSound("VoicedBilabialPlosive", "b", "common"))
	output.append(IpaSound("VoicelessLabiodentalPlosive", "p̪"))
	output.append(IpaSound("VoicedLabiodentalPlosive", "b̪"))
	output.append(IpaSound("VoicelessLinguolabialPlosive", "t̼"))
	output.append(IpaSound("VoicedLinguolabialPlosive", "d̼"))
	output.append(IpaSound("VoicelessAlveolarPlosive", "t", "common"))
	output.append(IpaSound("VoicedAlveolarPlosive", "d", "common"))
	output.append(IpaSound("VoicelessRetroflexPlosive", "ʈ"))
	output.append(IpaSound("VoicedRetroflexPlosive", "ɖ"))
	output.append(IpaSound("VoicelessPalatalPlosive", "c"))
	output.append(IpaSound("VoicedPalatalPlosive", "ɟ"))
	output.append(IpaSound("VoicelessVelarPlosive", "k", "common"))
	output.append(IpaSound("VoicedVelarPlosive", "g", "common"))
	output.append(IpaSound("VoicelessUvularPlosive", "q"))
	output.append(IpaSound("VoicedUvularPlosive", "ɢ"))
	output.append(IpaSound("EpiglottalPlosive", "ʡ"))
	output.append(IpaSound("GlottalStop", "ʔ"))
	output.append(IpaSound("VoicelessAlveolarSibilant", "s", "common"))
	output.append(IpaSound("VoicedAlveolarSibilant", "z"))
	output.append(IpaSound("VoicelessPostalveolarSibilant", "ʃ"))
	output.append(IpaSound("VoicedPostalveolarSibilant", "ʒ"))
	output.append(IpaSound("VoicelessRetroflexSibilant", "ʂ"))
	output.append(IpaSound("VoicedRetroflexSibilant", "ʐ"))
	output.append(IpaSound("VoicelessAlveolopalatalSibilant", "ɕ"))
	output.append(IpaSound("VoicedAlveolopalatalSibilant", "ʑ"))
	output.append(IpaSound("VoicelessBilabialFricative", "ɸ"))
	output.append(IpaSound("VoicedBilabialFricative", "β"))
	output.append(IpaSound("VoicelessLabiodentalFricative", "f", "common"))
	output.append(IpaSound("VoicedLabiodentalFricative", "v"))
	output.append(IpaSound("VoicelessLinguolabialFricative", "θ̼"))
	output.append(IpaSound("VoicedLinguolabialFricative", "ð̼"))
	output.append(IpaSound("VoicelessDentalFricatvie", "θ"))
	output.append(IpaSound("VoicedDentalFricative", "ð"))
	output.append(IpaSound("VoicelessAlveolarFricative", "θ̠"))
	output.append(IpaSound("VoicedAlveolarFricative", "ð̠"))
	output.append(IpaSound("VoicelessPostalveolarFricative", "ɹ̠̊˔"))
	output.append(IpaSound("VoicedPostalveolarFricative", "ɹ̠˔"))
	output.append(IpaSound("VoicelessRetroflexFricative", "ɻ̝̊"))
	output.append(IpaSound("VoicedRetroflexFricative", "ɻ̝"))
	output.append(IpaSound("VoicelessPalatalFricative", "ç"))
	output.append(IpaSound("VoicedPalatalFricative", "ʝ"))
	output.append(IpaSound("VoicelessVelarFricative", "x"))
	output.append(IpaSound("VoicedVelarFricative", "ɣ"))
	output.append(IpaSound("VoicelessUvularFricative", "χ"))
	output.append(IpaSound("VoicedUvularFricative", "ʁ"))
	output.append(IpaSound("VoicelessPharyngealFricative", "ħ"))
	output.append(IpaSound("VoicedPharyngealFricative", "ʕ"))
	output.append(IpaSound("VoicelessGlottalFricative", "h"))
	output.append(IpaSound("VoicedGlottalFricative", "ɦ"))
	output.append(IpaSound("VoicedLabiodentalApproximant", "ʋ"))
	output.append(IpaSound("VoicedAlveolarApproximant", "ɹ"))
	output.append(IpaSound("VoicedRetroflexApproximant", "ɻ"))
	output.append(IpaSound("VoicedPalatalApproximant", "j", "common"))
	output.append(IpaSound("VoicedVelarApproximant", "ɰ"))
	output.append(IpaSound("VoicedLabiodentalFlap", "ⱱ"))
	output.append(IpaSound("VoicedAlveolarFlap", "ɾ"))
	output.append(IpaSound("VoicedRetroflexFlap", "ɽ"))
	output.append(IpaSound("VoicedBilabialTrill", "ʙ"))
	output.append(IpaSound("VoicelessAlveolarTrill", "r̥"))
	output.append(IpaSound("VoicedAlveolarTrill", "r"))
	output.append(IpaSound("VoicelessUvularTrill", "ʀ̥"))
	output.append(IpaSound("VoicedUvularTrill", "ʀ"))
	output.append(IpaSound("VoicelssPharyngealTrill", "ʜ"))
	output.append(IpaSound("VoicedPharyngealTrill", "ʢ"))
	output.append(IpaSound("VoicelessAlveolarLateralFricative", "ɬ"))
	output.append(IpaSound("VoicedAlveolarLateralFricative", "ɮ"))
	output.append(IpaSound("VoicelessRetroflexLateralFricative", "ꞎ"))
	output.append(IpaSound("VoicedAlveolarLateralApproximant", "l", "common"))
	output.append(IpaSound("VoicedRetroflexLateralApproximant", "ɭ"))
	output.append(IpaSound("VoicedPalatalLateralApproximant", "ʎ"))
	output.append(IpaSound("VoicedVelarLateralApproximant", "ʟ"))
	output.append(IpaSound("VoicedUvularLateralApproximant", "ʟ̠"))
	output.append(IpaSound("VoicelessAlveolarLateralFlap", "ɺ̥"))
	output.append(IpaSound("VoicedAlveolarLateralFlap", "ɺ"))
	output.append(IpaSound("VoicedPalatalLateralFlap", "ʎ̆"))
	output.append(IpaSound("BilabialEjectiveStop", "pʼ"))
	output.append(IpaSound("AlveolarEjectiveStop", "tʼ"))
	output.append(IpaSound("RetroflexEjectiveStop", "ʈʼ"))
	output.append(IpaSound("PalatalEjectiveStop", "cʼ"))
	output.append(IpaSound("VelarEjectiveStop", "kʼ"))
	output.append(IpaSound("UvularEjectiveStop", "qʼ"))
	output.append(IpaSound("EpiglottalEjective", "ʡʼ"))
	output.append(IpaSound("BilabialEjectiveFricative", "ɸʼ"))
	output.append(IpaSound("LabiodentalEjectiveFricative", "fʼ"))
	output.append(IpaSound("DentalEjectiveFricative", "θʼ"))
	output.append(IpaSound("AlveolarEjectiveFricative", "sʼ"))
	output.append(IpaSound("PostalveolarEjectiveFricative", "ʃʼ"))
	output.append(IpaSound("RetroflexEjectiveFricative", "ʂʼ"))
	output.append(IpaSound("PalatalEjectiveFricative", "ɕʼ"))
	output.append(IpaSound("VelarEjectiveFricative", "xʼ"))
	output.append(IpaSound("UvularEjectiveFricative", "χʼ"))
	output.append(IpaSound("AlveolarLateralEjectiveFricative", "ɬʼ"))
	output.append(IpaSound("VoicelessBilabialClick", "k͡ʘ"))
	output.append(IpaSound("VoicelessDentalClick", "k͡ǀ"))
	output.append(IpaSound("VoicelessAlveolarClick", "k͡ǃ"))
	output.append(IpaSound("VoicelessPalatalClick", "k͡ǂ"))
	output.append(IpaSound("VoicedBilabialClick", "ɡ͡ʘ"))
	output.append(IpaSound("VoicedDentalClick", "ɡ͡ǀ"))
	output.append(IpaSound("VoicedAlveolarClick", "ɡ͡ǃ"))
	output.append(IpaSound("VoicedPalatalClick", "ɡ͡ǂ"))
	output.append(IpaSound("VoicedNasalBilabialClick", "ŋ͡ʘ"))
	output.append(IpaSound("VoicedNasalDentalClick", "ŋ͡ǀ"))
	output.append(IpaSound("VoicedNasalAlveolarClick", "ŋ͡ǃ"))
	output.append(IpaSound("VoicedNasalPalatalClick", "ŋ͡ǂ"))
	output.append(IpaSound("VoicelessLateralVelarClick", "k͡ǁ"))
	output.append(IpaSound("VoicedLateralVelarClick", "ɡ͡ǁ"))
	output.append(IpaSound("VoicedNasalLateralVelarClick", "ŋ͡ǁ"))
	output.append(IpaSound("VoicedBilabialImplosive", "ɓ"))
	output.append(IpaSound("VoicelessBilabialImplosive", "ɓ̥"))
	output.append(IpaSound("VoicedAlveolarImplosive", "ɗ"))
	output.append(IpaSound("VoicelessAlveolarImplosive", "ɗ̥"))
	output.append(IpaSound("VoicedPalatalImplosive", "ʄ"))
	output.append(IpaSound("VoicelessPalatalImplosive", "ʄ̊"))
	output.append(IpaSound("VoicedVelarImplosive", "ɠ"))
	output.append(IpaSound("VoicelessVelarImplosive", "ɠ̊"))
	output.append(IpaSound("VoicelessUvularImplosive", "ʛ̥"))
	output.append(IpaSound("VoicedLabialVelarApproximant", "w"))
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