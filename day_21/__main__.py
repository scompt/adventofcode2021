from typing import TextIO
import sys
import itertools

def read_input(textio:TextIO):
    lines = textio.readlines()
    player_1 = int(lines[0][-2:-1])
    player_2 = int(lines[1][-2:-1])
    return [player_1, player_2]

die = itertools.cycle(range(1,100+1))

positions = read_input(sys.stdin)
scores = [0,0]
turns = itertools.cycle(range(2))

for turn_num, player_num in enumerate(turns):
    positions[player_num] = (positions[player_num] + sum(next(die) for _ in range(3))) % 10
    if positions[player_num] == 0:
        scores[player_num] += 10
    else:
        scores[player_num] += positions[player_num]
    # print(player_num, positions[player_num], scores[player_num])
    if scores[player_num] >= 1000:
        break

print(min(scores) * (turn_num+1)*3)