from typing import TextIO, List, Dict, Union
import sys

CHARS = list('abcdefg')
DIGITS = {'abcefg':0, 'cf':1, 'acdeg':2, 'acdfg':3, 'bcdf':4, 'abdfg':5, 'abdefg':6, 'acf':7, 'abcdefg':8, 'abcdfg':9}
SEGMENTS = list(DIGITS.keys())
EASY = {2:1, 3:7, 4:4, 7:8}

def canonicalize(inp:Union[str,List[str]]):
    if type(inp) is str:
        return ''.join(sorted(inp))
    else:
        return [''.join(sorted(s)) for s in inp]

def print_mapping(mapping):
    for c in CHARS:
        print(c, mapping[c])

def read_input(textio: TextIO) -> List[int]:
    output = []
    for line in textio.readlines():
        before_str, after_str = line.strip().split(' | ')
        output.append((canonicalize(before_str.split(' ')), canonicalize(after_str.split(' '))))
    return output

def decode_mapping(signals:List[str]):
    forward_mapping:Dict[str:int] = dict()
    reverse_mapping:Dict[int:str] = dict()
    char_mapping = {c:set(CHARS) for c in CHARS}

    for signal in signals:
        for easy_in, easy_out in EASY.items():
            if len(signal) == easy_in:
                forward_mapping[signal] = easy_out
                reverse_mapping[easy_out] = signal

                for segment in SEGMENTS[easy_out]:
                    char_mapping[segment].intersection_update(signal)
    
    if 1 in reverse_mapping and 7 in reverse_mapping:
        a_segment = set(reverse_mapping[7])-set(reverse_mapping[1])
        char_mapping['a'] = a_segment
        for c, m in char_mapping.items():
            if c != 'a':
                m.difference_update(a_segment)

    if 1 in reverse_mapping and 4 in reverse_mapping:
        bd_segments = set(reverse_mapping[4])-set(reverse_mapping[1])
        char_mapping['b'].intersection_update(bd_segments)
        char_mapping['d'].intersection_update(bd_segments)

    for signal in signals:
        if len(signal) == 6:
            if not all(c in signal for c in char_mapping['c']):
                forward_mapping[signal] = 6
                reverse_mapping[6] = signal

            elif all(c in signal for c in char_mapping['b'].union(char_mapping['d'])):
                forward_mapping[signal] = 9
                reverse_mapping[9] = signal
            else:
                forward_mapping[signal] = 0
                reverse_mapping[0] = signal

        if len(signal) == 5:
            if all(c in signal for c in char_mapping['b'].union(char_mapping['d'])):
                forward_mapping[signal] = 5
                reverse_mapping[5] = signal
            
            elif all(c in signal for c in char_mapping['c'].union(char_mapping['f'])):
                forward_mapping[signal] = 3
                reverse_mapping[3] = signal

            else:
                forward_mapping[signal] = 2
                reverse_mapping[2] = signal
    return forward_mapping

lines = read_input(sys.stdin)

s = 0
for before, after in lines:
    mapping = decode_mapping(before + after)
    s += int(''.join(str(mapping[a]) for a in after))

print(s)