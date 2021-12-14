from collections import defaultdict
from typing import TextIO, Dict, Tuple
import sys
from operator import itemgetter

def read_input(textio: TextIO) -> Tuple[Dict[str, int], Dict[str, str], str]:
    lines = textio.readlines()
    
    counts = defaultdict(lambda: 0)
    template = lines[0].strip()
    for i in range(len(template)-1):
        pair = template[i:i+2]
        counts[pair] += 1

    rules = dict()
    for line in lines[2:]:
        pair, inserted = line.strip().split(' -> ')
        rules[pair] = inserted

    return counts, rules, template

def step(counts: Dict[str, int], rules: Dict[str, str]) -> str:
    out = defaultdict(lambda: 0)
    for rule_from, rule_to in rules.items():
        if rule_from in counts:
            count = counts[rule_from]
            out[rule_from[0]+rule_to] += count
            out[rule_to+rule_from[1]] += count
    return out

def stats(counts: Dict[str, int], template: str) -> Tuple[int, int]:
    char_counts = defaultdict(lambda: 0)
    for pair, count in counts.items():
        for char in pair:
            char_counts[char] += count
    char_counts[template[0]] += 1
    char_counts[template[-1]] += 1
    for char, count in char_counts.items():
        char_counts[char] = count//2
    return min(char_counts.items(), key=itemgetter(1))[1], max(char_counts.items(), key=itemgetter(1))[1]

counts, rules, template = read_input(sys.stdin)
for i in range(40):
    counts = step(counts, rules)

least_common, most_common = stats(counts, template)
print(most_common-least_common)