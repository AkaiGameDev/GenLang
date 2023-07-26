import morphologyGen
import phonologyGen
import json
import matplotlib.pyplot as plt
import zipf

# from json import JSONEncoder
# import numpy as np

def update_json_file():
    consonants = phonologyGen.create_all_ipa_consonants()
    output = []
    for c in consonants:
        output.append({
            'descriptiveName': c.descriptiveName,
            'ipaChar': c.ipaChar,
            'commonness': c.commonness,
            'phonation': c.phonation,
            'manner': c.manner,
            'place': c.place,
            'sound_type': c.sound_type
        })
    f = open('newIpaConsonants.json', 'w')
    json.dump(output, f, indent=2)


def ask_for_constraints():
    cons = []
    print("Enter constraints you would like the generator to have. Type 'help' for a list of commands")
    print('There is no validation yet so incorrectly entered constraints will simply be ignored')
    print("Type 'done' when you are done. Type 'list' for a list of constraints inputted thus far")
    print('...')
    while True:
        inp = input()
        if inp == 'done':
            return cons
        elif inp == 'help':
            print_command_list()
        elif inp == 'list':
            for c in cons:
                print(c)
        else:
            cons.append(inp)


def print_command_list():
    print('...')
    print('no: [restricted phoneme]')
    print('has: [required phoneme]')
    print('consonant inventory size: [number (default random)]')
    print('contrasting vowel lengths: [number (default 1)]')
    print('contrasting consonant lengths: [number (default 1)]')
    print('max syllables in morpheme: [number (default 3)]')
    print('starting consonant cluster sizes: [comma separated list of numbers]')
    print('vowel cluster sizes: [comma separated list of numbers]')
    print('ending consonant cluster sizes: [comma separated list of numbers]')
    print('...')


# def testExponential():
# 	data = np.random.exponential(scale=0.22, size=10000)
# 	plt.hist(data)
# 	plt.savefig('haha.png')

def test_zipfy_random():
    data = []
    for i in range(10):
        data.append(zipf.zipfy_random(5))
        print(data[i])
    plt.hist(data, bins=5)
    plt.savefig('zipfy.png')


if __name__ == '__main__':
    # test_zipfy_random()
    update_json_file()
    constraints = ask_for_constraints()
    phonology = phonologyGen.generate_phonology(constraints)
    phonologyGen.display_phonology(phonology)
    morphology = morphologyGen.generate_morphology(phonology, constraints)
    morphologyGen.display_morphology(morphology)
