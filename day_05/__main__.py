from typing import TextIO
import sys
from collections import namedtuple, defaultdict

Point = namedtuple("Point", ['x', 'y'])
Line = namedtuple("Line", ['from_point', 'to_point'])

def sign(val: int):
    if val < 0:
        return -1
    elif val > 0:
        return 1
    else:
        return 0

def generate_points(line: Line):    
    x_step = sign(line.to_point.x-line.from_point.x)
    y_step = sign(line.to_point.y-line.from_point.y)

    pos = line.from_point
    end = line.to_point
    while pos != end:
        yield pos
        pos = Point(pos.x+x_step, pos.y+y_step)
    yield end

def read_input(textio: TextIO):
    max_x = 0
    max_y = 0
    segments = []

    lines = textio.readlines()
    for line in lines:
        from_point_str, to_point_str = line.strip().split(" -> ")
        from_point = Point(*[int(coord) for coord in from_point_str.split(',')])
        to_point = Point(*[int(coord) for coord in to_point_str.split(',')])
        segments.append(Line(from_point, to_point))
        max_x = max(max_x, from_point.x, to_point.x)
        max_y = max(max_y, from_point.y, to_point.y)
    return segments, Point(max_x+1, max_y+1)

counts = defaultdict(lambda: 0)
lines, size = read_input(sys.stdin)
for line in lines:
    for point in generate_points(line):
        counts[point] += 1

print(sum(1 for _ in filter(lambda c: c>1, counts.values())))
