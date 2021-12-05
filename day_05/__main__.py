from typing import TextIO
import sys
from collections import namedtuple, defaultdict
from itertools import takewhile

Point = namedtuple("Point", ['x', 'y'])
Line = namedtuple("Line", ['from_point', 'to_point'])

def generate_points(line: Line):
    if not(line.from_point.x == line.to_point.x) and not(line.from_point.y == line.to_point.y):
        return

    min_x = min(line.from_point.x, line.to_point.x)
    max_x = max(line.from_point.x, line.to_point.x)
    min_y = min(line.from_point.y, line.to_point.y)
    max_y = max(line.from_point.y, line.to_point.y)
    
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            yield Point(x, y)
        

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
    points = list(generate_points(line))
    
    for point in generate_points(line):
        counts[point] += 1

print(sum(1 for _ in filter(lambda c: c>1, counts.values())))
