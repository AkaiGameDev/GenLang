import math
import random
import numpy as np
import zipf


class Syllable:
    def __init__(self, pronunciation):
        self.pronunciation = pronunciation

    def __str__(self):
        output = ""
        for s in self.pronunciation:
            output += str(s)
        return output


class Morpheme:
    # morphemeType can be:
    # freeLexical
    # freeFunctional
    # boundPrefix
    # boundAffix
    def __init__(self, syllables, morpheme_type, meaning):
        self.syllables = syllables
        self.morphemeType = morpheme_type
        self.meaning = meaning
        self.pronunciation = ""
        for s in syllables:
            self.pronunciation += str(s)

    def __str__(self):
        output = ""
        for s in self.pronunciation:
            output += str(s)
        return output

    def __repr__(self):
        return f'{str(self)} is a morpheme of type {self.morphemeType} with the meaning: {self.meaning}'


def generate_morpheme_from_meaning(phonology, morphology, morpheme_type, meaning, constraints=None):
    # default values
    max_syllables = 3
    # check for constraints
    if constraints is None:
        constraints = []
    else:
        for c in constraints:
            if 'max syllables in morpheme:' in c:
                max_syllables = int(c.replace('max syllables in morpheme:', '').strip())

    # select a number of syllables skewed towards having fewer syllables using an zipf-y distribution
    selected_syllable_count = zipf.zipfy_random(max_syllables) + 1

    # generate syllables
    morph_syllables = []
    for i in range(selected_syllable_count):
        morph_syllables.append(generate_syllable(phonology, constraints))

    return Morpheme(morph_syllables, morpheme_type, meaning)


def generate_syllable_from_structure(phonology, structure, constraints=None):
    # Note: the structure parameter here looks very similar to other representations of syllable structure but differ
    # in a meaningful way It is still a string of 'c' and 'v', but this representation allows for multiple v's in a
    # row representative of diphthongs, triphthongs, or lengthened vowels. Most other representations of vowel
    # structures you will encounter will use one 'v' for those cases
    if constraints is None:
        constraints = []
    pronunciation = []
    consonants = phonology[0]
    vowels = phonology[1]

    # constraints checking
    contrasting_vowel_lengths = 1
    contrasting_consonant_lengths = 1
    for c in constraints:
        if "contrasting vowel length:" in c:
            contrasting_vowel_lengths = int(c.replace("contrasting vowel length:", "").trim())
        elif "contrasting consonant length:" in c:
            contrasting_consonant_lengths = int(c.replace("contrasting consonant length:", "").trim())

    for sound in structure:
        if sound == 'c':
            # used for validating constraints
            picked_consonant = None
            need_repick = True
            while need_repick:
                picked_consonant = consonants[math.floor(random.random() * len(consonants))]
                # check if the previous contrastingConsonantLengths number of consonants are the same
                if len(pronunciation) < 2:
                    need_repick = False
                else:
                    # start from end of list and iterate backwards contrasingConsonantLenghths times
                    for i in range(len(pronunciation) - 1, len(pronunciation) - (contrasting_consonant_lengths + 1),
                                   -1):
                        if pronunciation[i] != picked_consonant:
                            need_repick = False
                            break
            pronunciation.append(picked_consonant)
        picked_vowel = None
        if sound == 'v':
            # repick vowels until constraints satisfied
            # used for validating constraints
            need_repick = True
            while need_repick:
                picked_vowel = vowels[math.floor(random.random() * len(vowels))]
                # check if the previous contrastingVowelLengths number of vowels are the same
                if len(pronunciation) <= contrasting_vowel_lengths:
                    need_repick = False
                    break
                else:
                    # start from end of list and iterate backwards contrasingVowelLenghths times
                    for i in range(len(pronunciation) - 1, len(pronunciation) - (contrasting_vowel_lengths + 1), -1):
                        if pronunciation[i] != picked_vowel:
                            need_repick = False
                            break
            pronunciation.append(picked_vowel)
    return Syllable(pronunciation)


def generate_syllable(phonology, constraints=None):
    # default values
    # these list all possible cluster sizes in descending order of commonness following a zipfy distribution
    # these default values should match somewhat to English and other similar languages
    possible_starting_consonant_cluster_sizes = [1, 0, 2, 3]
    possible_vowel_cluster_sizes = [1, 2, 3]
    possible_ending_consonant_cluster_sizes = [0, 1, 2, 3, 4]
    if constraints is None:
        constraints = []
    else:
        for c in constraints:
            if 'starting consonant cluster sizes:' in c:
                input_strings = c.replace('starting consonant cluster sizes:', '').replace(' ', '').split(',')
                possible_starting_consonant_cluster_sizes = []
                for s in input_strings:
                    possible_starting_consonant_cluster_sizes.append(int(s))
            elif 'vowel cluster sizes:' in c:
                input_strings = c.replace('vowel cluster sizes:', '').replace(' ', '').split(',')
                possible_vowel_cluster_sizes = []
                for s in input_strings:
                    possible_vowel_cluster_sizes.append(int(s))
            elif 'ending consonant cluster sizes:' in c:
                input_strings = c.replace('ending consonant cluster sizes:', '').replace(' ', '').split(',')
                possible_ending_consonant_cluster_sizes = []
                for s in input_strings:
                    possible_ending_consonant_cluster_sizes.append(int(s))

    # using a zipfy distribution that feels more natural than other distributions tested
    # tested uniform and exponential distributions
    starting_possibilities = len(possible_starting_consonant_cluster_sizes)
    if starting_possibilities == 1:
        starting_cluster_size = possible_starting_consonant_cluster_sizes[0]
    elif starting_possibilities > 1:
        starting_cluster_size = possible_starting_consonant_cluster_sizes[zipf.zipfy_random(starting_possibilities)]
    else:
        raise 'possible_starting_consonant_cluster_sizes empty'

    vowel_possibilities = len(possible_vowel_cluster_sizes)
    if vowel_possibilities == 1:
        vowel_cluster_size = possible_vowel_cluster_sizes[0]
    elif vowel_possibilities > 1:
        vowel_cluster_size = possible_vowel_cluster_sizes[zipf.zipfy_random(vowel_possibilities)]
    else:
        raise 'possible_vowel_cluster_sizes empty'

    ending_possibilities = len(possible_ending_consonant_cluster_sizes)
    if ending_possibilities == 1:
        ending_cluster_size = possible_ending_consonant_cluster_sizes[0]
    elif ending_possibilities > 1:
        ending_cluster_size = possible_ending_consonant_cluster_sizes[zipf.zipfy_random(ending_possibilities)]
    else:
        raise 'possible_ending_consonant_cluster_sizes empty'

    # generate structure to pass to generateSyllableFromStructure()
    structure = ""
    for i in range(starting_cluster_size):
        structure += 'c'
    for i in range(vowel_cluster_size):
        structure += 'v'
    for i in range(ending_cluster_size):
        structure += 'c'

    return generate_syllable_from_structure(phonology, structure, constraints)


def generate_morphology(phonology, constraints=None):
    if constraints is None:
        constraints = []
    morphology = []
    for i in range(30):
        morphology.append(
            generate_morpheme_from_meaning(phonology, morphology, "freeLexical", "nomeaning", constraints))

    return morphology


def display_morphology(morphology):
    for m in morphology:
        # print(f'{str(m)} is a morpheme of sound_type {m.morphemeType} with the meaning: {m.meaning}')
        print(repr(m))
