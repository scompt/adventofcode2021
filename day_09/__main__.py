from typing import TextIO, List, Dict, Tuple
import sys
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

def read_input(textio: TextIO) -> Tuple[Dict[Point, int], Point]:
    max_x = max_y = 0
    output = dict()
    for y, line in enumerate(textio.readlines()):
        max_y = max(y, max_y)
        for x, height in enumerate(line.strip()):
            max_x = max(x, max_x)
            output[Point(x=x,y=y)] = int(height)
    return output, Point(x=max_x, y=max_y)

def find_minima(heightmap: Dict[Point, int], bounds: Point) -> List[Point]:
    minima = []
    for y in range(bounds.y+1):
        for x in range(bounds.x+1):
            location = Point(x=x,y=y)
            if is_minimum(heightmap, location):
                minima.append(location)
    return minima

def is_minimum(heightmap: Dict[Point, int], location: Point) -> bool:
    try:
        height = heightmap[location]
    except KeyError:
        return False

    for x_delta, y_delta in [(0,1), (0, -1), (1,0), (-1,0)]:
        try:
            neighbor_height = heightmap[Point(location.x+x_delta, location.y+y_delta)]
            if neighbor_height <= height:
                return False
        except KeyError:
            continue
    
    return True

def risk_level(heightmap: Dict[Point, int], minima: List[Point]) -> int:
    score = len(minima)
    for location in minima:
        score += heightmap[location]
    return score

def print_heightmap(heightmap: Dict[Point, int], bounds: Point, minima: List[Point]):
    for y in range(bounds.y+1):
        for x in range(bounds.x+1):
            location = Point(x=x,y=y)
            if location in minima:
                print('\033[1m', end='')
            print(heightmap[location], end='')
            if location in minima:
                print('\033[0m', end='')
        print()

heightmap, bounds = read_input(sys.stdin)
minima = find_minima(heightmap, bounds)
score = risk_level(heightmap, minima)
# print_heightmap(heightmap, bounds, minima)
print(score)
