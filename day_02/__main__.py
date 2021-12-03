from typing import TextIO, List, Tuple
import sys
from utils import read_lines

depth = 0
horiz = 0
aim = 0

lines = read_lines(sys.stdin, {"axis": str, "distance": int})
for line in lines:
    if line['axis'] == 'up':
        aim -= line['distance']
    elif line['axis'] == 'down':
        aim += line['distance']
    elif line['axis'] == 'forward':
        horiz += line['distance']
        depth += aim * line['distance']
print(depth * horiz)
