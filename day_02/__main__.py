from typing import TextIO, List, Tuple

def read_lines(textio: TextIO) -> List[Tuple[int]]:
    depth = 0
    horiz = 0
    aim = 0
    lines = textio.readlines()
    for line in [l.strip() for l in lines]:
        axis, distance = line.split(' ', 1)
        distance = int(distance)
        print(axis, distance)
        if axis == 'up':
            aim -= distance
        elif axis == 'down':
            aim += distance
        elif axis == 'forward':
            horiz += distance
            depth += aim * distance
        print(depth, horiz, depth * horiz)

if __name__ == "__main__":
    import sys
    read_lines(sys.stdin)
