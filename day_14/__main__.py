from collections import defaultdict
from typing import TextIO, Dict, Tuple
import sys
from operator import itemgetter

def read_input(textio: TextIO) -> Tuple[str, Dict[str, str]]:
    lines = textio.readlines()
    template = lines[0].strip()
    rules = dict()

    for line in lines[2:]:
        pair, inserted = line.strip().split(' -> ')
        rules[pair] = inserted

    return template, rules

def step(template: str, rules: Dict[str, str]) -> str:
    out = ""
    for i in range(len(template)-1):
        pair = template[i:i+2]
        out += pair[0]
        out += rules[pair]
    out += template[-1]
    return out

def stats(template: str) -> Tuple[int, int]:
    counts = defaultdict(lambda: 0)
    for char in template:
        counts[char] += 1
    
    return min(counts.items(), key=itemgetter(1))[1], max(counts.items(), key=itemgetter(1))[1]

template, rules = read_input(sys.stdin)
for i in range(10):
    template = step(template, rules)

least_common, most_common = stats(template)
print(most_common-least_common)