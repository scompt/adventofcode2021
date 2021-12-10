from typing import TextIO, List, Dict, Tuple, Set
import sys
from collections import namedtuple, defaultdict

PAIRS = {'(':')', '{':'}', '<':'>', '[':']'}
OPENERS = list(PAIRS.keys())
CLOSERS = list(PAIRS.values())
SCORES = {')':3, '}':1197, '>':25137, ']':57}

def read_line(line: str):
    """
    >>> read_line('([])')
    (True, [])
    """
    chars = []
    for char in line.strip():
        if char in OPENERS:
            chars.insert(0, char)
        elif char in CLOSERS:
            if len(chars) == 0:
                return False, [char]
            elif PAIRS[chars[0]] != char:
                return False, [char]
            else:
                chars.pop(0)
        else:
            return False, [char]
    return True, chars

def read_input(textio: TextIO):
    score = 0
    lines = textio.readlines()
    for line in lines:
        legal, chars = read_line(line)
        if not legal:
            score += SCORES[chars[0]]
    return score

print(read_input(sys.stdin))
