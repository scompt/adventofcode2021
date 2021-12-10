from typing import TextIO, List, Dict, Tuple, Set
import sys
from collections import namedtuple, defaultdict

PAIRS = {'(':')', '{':'}', '<':'>', '[':']'}
OPENERS = list(PAIRS.keys())
CLOSERS = list(PAIRS.values())
ILLEGAL_SCORES = {')':3, '}':1197, '>':25137, ']':57}
INCOMPLETE_SCORES = {')':1, '}':3, '>':4, ']':2}

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
                raise Exception()
            elif PAIRS[chars[0]] != char:
                return False, ILLEGAL_SCORES[char]
            else:
                chars.pop(0)
        else:
            raise Exception()
    return True, score_incompleted(chars)

def score_incompleted(chars):
    score = 0
    for char in chars:
        score = score * 5
        score = score + INCOMPLETE_SCORES[PAIRS[char]]
    return score

def read_input(textio: TextIO):
    score = 0
    lines = textio.readlines()
    incomplete = []
    for line in lines:
        legal, line_score = read_line(line)
        if not legal:
            score += line_score
        elif legal:
            incomplete.append(line_score)
    incomplete.sort()
    return score, incomplete[len(incomplete)//2]

print(read_input(sys.stdin))
