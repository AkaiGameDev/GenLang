import sys
import types
from phonologyGen import *
from wordGen import *
import json
from json import JSONEncoder

def testWordGen():
    # select sounds
    phonology = generatePhonologyNormal()
    printPhonology(phonology)

    selectedWords = []

    for i in range(10):
        selectedWords.append(generateWord(phonology, "nomeaning"))

    print(f"Generated {len(selectedWords)} words:")
    for w in selectedWords:
        print(w)

def testPhonologyGen():
    # select sounds
    phonology = generatePhonologyNormal()
    printPhonology(phonology) 

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

def imports():
    imp = []
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            imp.append(val.__name__)
    return imp

def showDependencies():
    print (sys.modules.keys())
    print ("Modules:\n")
    print (imports())
    

if __name__ == '__main__':
    # create3VowelSystem()
    # create5VowelSystem()
    testWordGen()
    # testPhonologyGen()

