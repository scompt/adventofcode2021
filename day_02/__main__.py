from typing import TextIO, List, Tuple

def read_lines(textio: TextIO) -> List[Tuple[int]]:
    depth = 0
    horiz = 0
    lines = textio.readlines()
    for line in [l.strip() for l in lines]:
        axis, distance = line.split(' ', 1)
        distance = int(distance)
        print(axis, distance)
        if axis == 'up':
            depth -= distance
        elif axis == 'down':
            depth += distance
        elif axis == 'forward':
            horiz += distance
        print(depth, horiz, depth * horiz)

if __name__ == "__main__":
    import sys
    read_lines(sys.stdin)
