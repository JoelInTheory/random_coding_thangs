"""
Accepts a dot-dash representation of a morse code message, without breaks between letters
prints all possible character combinations that could be used to create that string

This was a coding exercise, please don't use this to make actual morse code messages.
Especially if your life depends on it.

"""
from sys import argv



CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }

LETTER_SEPERATOR = ''

string = argv[1]

def make_signals(input_string):
    output = []
    for char in input_string:
        output.append(CODE[char])
    return LETTER_SEPERATOR.join(output)

def checkstart(my_string, existing = ''):
    chars = []
    if existing != '':
        existing_signals = make_signals(existing)
        my_string = my_string.split(existing_signals, 1)[1]
    for CHAR, signals in CODE.iteritems():
        if my_string.startswith(signals):
            chars.append(existing + CHAR)
    return chars

def check_string(my_string):
    final = []
    possibles = checkstart(my_string)
    while possibles:
        possible = possibles.pop(0)
        if make_signals(possible) == my_string:
            final.append(possible)
        else:
            new_possibles = checkstart(string, existing = possible)
            possibles = possibles + new_possibles
    return final

final_words = check_string(string)
print sorted(final_words)
