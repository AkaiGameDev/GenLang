# This script is used to generate a phonology

# Current Version:
# The generator first decides how many consonants are going to be in this phonology
# Then it picks the most common consonants at random
# After the list of common consonants are exhausted, it picks the other consonants at random
# It decides either to use a 3 vowel system or a 5 vowel system
# These systems have predetermined vowels

# The vowel system does not include the diphthongs that can be created from them
# diphthongs, triphthongs, and lengthened vowels will be handled as multiple vowels in a row by morphology

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
    def __init__(self, descriptive_name, ipaChar, commonness, phonation, manner, place, sound_type):
        super().__init__(descriptive_name, ipaChar)
        self.commonness = commonness
        self.phonation = phonation
        self.manner = manner
        self.place = place
        self.sound_type = sound_type
    def __repr__(self):
        myStr = f'IPA character:     {self.ipaChar}\n'
        myStr += f'Descriptive name: {self.descriptiveName}\n'
        myStr += f'Place of Artic.:  {self.place}\n'
        myStr += f'Manner:           {self.manner}\n'
        return myStr

# class IpaVowel(IpaSound):
#     def __init__(self, descriptiveName, ipaChar, height, roundedness, backness):
#         self.descriptiveName = descriptiveName
#         self.ipaChar = ipaChar
#         self.sound_type = sound_type
# 
#     def __repr__(self):
#         return f'This sound\'s IPA character is {self.ipaChar}, its descriptive name is {self.descriptiveName}, ' \
#                f'\nits place of articulation is {self.place}, and its manner of articulation is {self.manner}'
# 

class IpaVowel(IpaSound):
    def __init__(self, descriptive_name, ipaChar, height, roundedness, backness):
        super().__init__(descriptive_name, ipaChar)
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
    if (category < 89):    # Small (6 - 14)
        count = math.floor(random.random() * 9) + 6
    elif (category < (89 + 122)):    # Moderately Small (15 - 18)
        count = math.floor(random.random() * 4) + 15
    elif (category < (89 + 122 + 201)):    # Average (19 - 25)
        count = math.floor(random.random() * 7) + 19
    elif (category < (89 + 122 + 201 + 94)):    # Moderately Large (26 - 33)
        count = math.floor(random.random() * 8) + 26
    else:    # Large (34 - 122)
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

    trim_table(pulmonicConsonants)

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

def create_all_ipa_consonants():
    # TODO: finish adding consonants
    # Create a list with the consonants from this page:
    # https://en.wikipedia.org/wiki/International_Phonetic_Alphabet#Consonants
    # consonants described as 'extremely rare' are excluded
    # consonants described as likely only existing in allophones are also excluded
    f = open('ipaConsonants.json', 'r')
    data = f.read()
    data.encode('unicode_escape')
    dicts = json.loads(data)
    f.close()
    output = []
    for d in dicts:
        output.append(
            IpaConsonant(d['descriptive_name'], d['ipa_char'], d['commonness'], d['phonation'], d['manner'], d['place'],
                         d['sound_type']))
    return output


def create_all_ipa_vowels():
    f = open('ipaVowels.json', 'r')
    dicts = json.load(f)
    f.close()
    output = []
    for d in dicts:
        output.append(IpaVowel(d['descriptive_name'], d['ipa_char'], d['height'], d['roundedness'], d['backness']))
    return output


def create_3_vowel_system():
    allvowels = create_all_ipa_vowels()
    output = []
    for v in allvowels:
        if v.ipaChar == 'i' or v.ipaChar == 'u' or v.ipaChar == 'a':
            output.append(v)
    return output


def create_5_vowel_system():
    all_vowels = create_all_ipa_vowels()
    output = []
    for v in all_vowels:
        if v.ipaChar == 'i' or v.ipaChar == 'u' or v.ipaChar == 'e' or v.ipaChar == 'o' or v.ipaChar == 'a':
            output.append(v)
    return output


def select_consonants(constraints=None):
    # Follows distribution shown here: https://wals.info/chapter/1

    if constraints is None:
        constraints = []
    working_consonants = create_all_ipa_consonants()
    # remove restricted consonants based on constraints
    for constraint in constraints:
        if 'no:' in constraint:
            # attempt to remove if it exists
            to_be_removed = constraint.replace('no:', '').strip()
            for consonant in working_consonants:
                if to_be_removed == consonant.ipaChar or to_be_removed == consonant.descriptiveName:
                    working_consonants.remove(consonant)

    # Consonant inventory size selection
    # Listen to constraint specification if it exists, if not pick at random using following method:
    # Decide which category we fall under, then pick a random number in that range
    # Every category other than large has a uniform distribution
    # Large has an exponential distribution to make extremely high inventories less likely

    size_specified = False
    for c in constraints:
        if 'consonant inventory size:' in c:
            size_specified = True
            count = int(c.replace('consonant inventory size:', '').strip())

    if not size_specified:
        category = math.floor(random.random() * 563)
        if category < 89:  # Small (6 - 14)
            count = math.floor(random.random() * 9) + 6
        elif category < (89 + 122):  # Moderately Small (15 - 18)
            count = math.floor(random.random() * 4) + 15
        elif category < (89 + 122 + 201):  # Average (19 - 25)
            count = math.floor(random.random() * 7) + 19
        elif category < (89 + 122 + 201 + 94):  # Moderately Large (26 - 33)
            count = math.floor(random.random() * 8) + 26
        else:  # Large (34 - 122)
            # uses a different distribution to skew selection towards smaller side
            count = math.floor(np.random.exponential(scale=0.2) * 89) + 34
        if count > len(working_consonants):
            count = len(working_consonants)

    # Pick consonants
    # Note: if there are more 'has:' constraints than 'consonant inventory size:' specifies,
    # we will include all 'has:' constraints instead of adhering to 'consonant inventory size:'
    output = []
    # insert any consonants specified by constraints
    for constraint in constraints:
        if 'has:' in constraint:
            # check if what follows is in working_consonants
            # note: this means no: will take priority over has: in conflicting constraints
            to_be_added = constraint.replace('has:', '').strip()
            for consonant in working_consonants:
                if to_be_added == consonant.ipaChar or to_be_added == consonant.descriptiveName:
                    output.append(consonant)

    # Make a list of consonants with the common tag
    common_consonants = []
    for s in working_consonants:
        if s.commonness == 'common':
            common_consonants.append(s)
    # pick common consonants first
    for i in range(count):
        if len(common_consonants) > 0:
            pick_index = math.floor(random.random() * len(common_consonants))
            output.append(common_consonants[pick_index])
            working_consonants.remove(common_consonants[pick_index])
            common_consonants.pop(pick_index)
        else:
            pick_index = math.floor(random.random() * len(working_consonants))
            output.append(working_consonants[pick_index])
            working_consonants.pop(pick_index)

    return output


def select_vowels(constraints=None):
    all_vowels = create_all_ipa_vowels()
    selected_vowels = []
    vowel_inventory_size = None
    if constraints is not None:
        for c in constraints:
            if 'vowel inventory size:' in c:
                vowel_inventory_size = c.replace('vowel inventory size:', '').strip()
            elif 'has:' in c:
                to_be_added = c.replace('has:', '').strip()
                # find matching vowel in all_vowels
                for v in all_vowels:
                    if v.ipaChar == to_be_added or v.descriptiveName == to_be_added:
                        selected_vowels.append(v)
            elif 'no:' in c:
                to_be_removed = c.replace('no:', '').strip()
                for v in all_vowels:
                    if v.ipaChar == to_be_removed or v.descriptiveName == to_be_removed:
                        all_vowels.remove(v)

    if vowel_inventory_size == None:
        if random.random() < 0.5:
            vowel_inventory_size = 3
        else:
            vowel_inventory_size = 5

    if len(selected_vowels) == 0 and vowel_inventory_size == 3:
        return create_3_vowel_system()
    elif len(selected_vowels) == 0 and vowel_inventory_size == 5:
        return create_5_vowel_system()

    while len(selected_vowels) < vowel_inventory_size:
        # select a vowel that is as far away from the others as possible
        selected_vowels.append(select_furthest_vowel(selected_vowels, all_vowels))

def select_furthest_vowel(selected_vowels, all_vowels):
    distances = {}
    for av in all_vowels:
        current_vowel_distance = 0
        is_duplicate = False
        for sv in selected_vowels:
            if av == sv:
                is_duplicate = True
                break
            else:
                current_vowel_distance += distance_between_vowels(av, sv)
        if not is_duplicate:
            distances[av] = current_vowel_distance

    # pick furthest vowel
    furthest_distance = 0
    furthest_vowel = None
    for d in distances:
        if distances[d] > furthest_distance:
            furthest_distance = distances[d]
            furthest_vowel = d

    return furthest_vowel

def distance_between_vowels(v1, v2):
    v1_height_value = None
    v1_backness_value = None


def generate_phonology(constraints=None):
    if constraints is None:
        constraints = []
    selected_consonants = select_consonants(constraints)
    selected_vowels = select_vowels(constraints)
    return selected_consonants, selected_vowels


def display_phonology(phonology):
    consonants = phonology[0]
    vowels = phonology[1]
    display_pulmonic_consonants(consonants)
    display_nonpulmonic_consonants(consonants)
    display_vowels(vowels)


def display_pulmonic_consonants(consonants):
    pulmonic_consonants = [
        ['', 'Bilabial', 'Labio-dental', 'Linguo-labial', 'Dental', 'Alveolar', 'Post-alveolar', 'Retro-flex',
         'Palatal', 'Velar', 'Uvular', 'Pharyngeal/epiglottal', 'Glottal'],
        ['Nasal', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', '']],
        ['Plosive', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', '']],
        ['Sibilant fricative', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', ''], ['', '']],
        ['Non-sibilant fricative', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', ''], ['', ''], ['', '']],
        ['Approximant', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', ''], ['', '']],
        ['Tap/flap', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', '']],
        ['Trill', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', '']],
        ['Lateral fricative', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', ''], ['', '']],
        ['Lateral approximant', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', ''], ['', ''], ['', '']],
        ['Lateral tap/flap', ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''],
         ['', ''], ['', ''], ['', '']]]

    pulmonic_place_dict = {
        'bilabial': 'Bilabial',
        'labiodental': 'Labio-dental',
        'linguolabial': 'Linguo-labial',
        'dental': 'Dental',
        'alveolar': 'Alveolar',
        'postalveolar': 'Post-alveolar',
        'retroflex': 'Retro-flex',
        'palatal': 'Palatal',
        'velar': 'Velar',
        'uvular': 'Uvular',
        'pharyngeal': 'Pharyngeal/epiglottal',
        'glottal': 'Glottal'
    }

    pulmonic_manner_dict = {
        'nasal': 'Nasal',
        'plosive': 'Plosive',
        'sibilant': 'Sibilant fricative',
        'fricative': 'Non-sibilant fricative',
        'approximant': 'Approximant',
        'flap': 'Tap/flap',
        'trill': 'Trill',
        'lateralfricative': 'Lateral fricative',
        'lateralapproximant': 'Lateral approximant',
        'lateralflap': 'Lateral tap/flap'
    }

    row_headers = []
    for r in pulmonic_consonants:
        row_headers.append(r[0])

    for c in consonants:
        if c.sound_type == 'pulmonic':
            column = pulmonic_consonants[0].index(pulmonic_place_dict[c.place[0]])
            row = row_headers.index(pulmonic_manner_dict[c.manner[0]])
            if c.phonation == 'voiceless':
                pulmonic_consonants[row][column][0] = c.ipaChar
            elif c.phonation == 'voiced':
                pulmonic_consonants[row][column][1] = c.ipaChar
            else:
                print(f'{c.descriptiveName} has a phonation that is not set correctly')

    format_pairs_in_table(pulmonic_consonants)
    pulmonic_consonants = trim_table(pulmonic_consonants)

    if len(pulmonic_consonants) > 1:
        print('Pulmonic Consonants')
        print('In places where letters appear in pairs, the letter to the right represents a voiced consonant')
        print('and the letter to the left represents an unvoiced consonant')
        print('In places where letters appear by themselves, the letter represents a voiced consonant')
        print(tabulate(pulmonic_consonants, tablefmt='simple_grid'))


def display_nonpulmonic_consonants(consonants):
    output = [
        ['', '', 'Bilabial', 'Labio-dental', 'Dental', 'Alveolar', 'Post-alveolar', 'Retro-flex', 'Palatal', 'Velar',
         'Uvular', 'Pharyngeal/epiglottal'],
        ['Ejective', 'Stop'],
        ['Ejective', 'Fricative'],
        ['Ejective', 'Lateral fricative'],
        ['Click', 'Tenuis'],
        ['Click', 'Voiced'],
        ['Click', 'Nasal'],
        ['Click', 'Tenuis lateral'],
        ['Click', 'Voiced lateral'],
        ['Click', 'Nasal lateral'],
        ['Implosive', 'Voiced'],
        ['Implosive', 'Voiceless']]

    column_count = len(output[0])
    for i, r in enumerate(output):
        while len(r) < column_count:
            output[i].append('')

    place_dict = {
        'bilabial': 'Bilabial',
        'labiodental': 'Labio-dental',
        'linguolabial': 'Linguo-labial',
        'dental': 'Dental',
        'alveolar': 'Alveolar',
        'postalveolar': 'Post-alveolar',
        'retroflex': 'Retro-flex',
        'palatal': 'Palatal',
        'velar': 'Velar',
        'uvular': 'Uvular',
        'pharyngeal': 'Pharyngeal/epiglottal',
        'glottal': 'Glottal'
    }

    for c in consonants:
        if c.sound_type == 'nonpulmonic':
            # find row
            if 'ejective' in c.manner:
                if 'plosive' in c.manner:
                    row = 1
                # this is out of order because fricative is in lateralfricative
                elif 'lateralfricative' in c.manner:
                    row = 3
                elif 'fricative' in c.manner:
                    row = 2
                else:
                    print(f'error finding row for {c.ipaChar}')
                    exit()
            # this is also out of order for a similar reason as above
            elif 'lateralclick' in c.manner:
                if c.phonation == 'voiceless':
                    row = 7
                elif c.phonation == 'voiced' and 'nasal' in c.manner:
                    row = 9
                elif c.phonation == 'voiced' and 'nasal' not in c.manner:
                    row = 8
                else:
                    print(f'error finding row for {c.ipaChar}')
                    exit()
            elif 'click' in c.manner:
                if c.phonation == 'voiceless':
                    row = 4
                elif c.phonation == 'voiced' and 'nasal' in c.manner:
                    row = 6
                elif c.phonation == 'voiced' and 'nasal' not in c.manner:
                    row = 5
                else:
                    print(f'error finding row for {c.ipaChar}')
                    exit()
            elif 'implosive' in c.manner:
                if c.phonation == 'voiced':
                    row = 10
                elif c.phonation == 'voiceless':
                    row = 11
                else:
                    print(f'error finding row for {c.ipaChar}')
                    exit()
            else:
                print(f'error finding row for {c.ipaChar}')
                exit()

            # find column
            if 'lateralclick' in c.manner:
                column = 5
            elif 'click' in c.manner:
                for p in c.place:
                    if not p == 'velar':
                        if p == 'bilabial':
                            column = 2
                        elif p == 'dental':
                            column = 4
                        elif p == 'alveolar':
                            column = 5
                        elif p == 'palatal':
                            column = 8
            elif 'ejective' in c.manner or 'implosive' in c.manner:
                column = output[0].index(place_dict[c.place[0]])
            else:
                print(f'error finding column for {c.ipaChar}')
                exit()

            output[row][column] = c.ipaChar

    output = trim_table(output, header_columns=2)

    if len(output) > 1:
        print('Non-pulmonic Consonants')
        print(tabulate(output, tablefmt='simple_grid'))


def display_vowels(vowels):
    print(f'This phonology has {len(vowels)} vowels. They are:')
    for v in vowels:
        print(str(v))


def format_pairs_in_table(table):
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

def trim_table(table, header_rows=1, header_columns=1):
    output = trim_rows(table, header_columns)
    output = trim_columns(output, header_rows)
    return output


def trim_rows(table, header_columns):
    empty_row_indices = []
    for r in table:
        is_empty = True
        for e in r:
            if e != '' and r.index(e) >= header_columns:
                is_empty = False
        if is_empty:
            empty_row_indices.append(table.index(r))

    for i in reversed(empty_row_indices):
        table.remove(table[i])

    return table


def trim_columns(table, header_rows):
    empty_column_indices = []
    for i in range(len(table[0])):
        is_empty = True
        for r in table:
            if r[i] != '' and table.index(r) >= header_rows:
                is_empty = False
        if is_empty:
            empty_column_indices.append(i)

    for i in reversed(empty_column_indices):
        for j, r in enumerate(table):
            table[j].pop(i)

    return table

def printPhonology(phonology):
    selectedConsonants = phonology[0]
    selectedVowels = phonology[1]
    print(f'selected {len(selectedConsonants)} consonants and {len(selectedVowels)} vowels.')
    print("Consonants:")
    for c in selectedConsonants:
        print(repr(c))
        print()

    print("Vowels:")
    for v in selectedVowels:
        print(repr(v))
    print()


