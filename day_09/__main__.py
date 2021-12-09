from typing import TextIO, List, Dict, Tuple, Set
import sys
from collections import namedtuple, defaultdict
import functools
import operator

Point = namedtuple("Point", ['x', 'y'])

def read_input(textio: TextIO) -> Tuple[Dict[Point, int], Point]:
    output = dict()
    lines = textio.readlines()
    for y, line in enumerate(lines):
        line = line.strip()
        for x, height in enumerate(line):
            output[Point(x=x,y=y)] = int(height)
    return output, Point(x=len(line), y=len(lines))

def find_basins(heightmap: Dict[Point, int], size: Point) -> List[Set[Point]]:
    basins: List[Set[Point]] = []
    reverse_basin: Dict[Point, int] = dict()

    for y in range(size.y):
        for x in range(size.x):
            location = Point(x=x,y=y)
            if heightmap[location] == 9:
                continue

            basin_number = None
            for neighbor in neighbors(location):
                try:
                    neighbor_height = heightmap[neighbor]
                    if neighbor_height == 9:
                        continue
                except KeyError:
                    continue

                try:
                    basin_number = reverse_basin[neighbor]
                except KeyError:
                    continue

                basins[basin_number].add(location)
                reverse_basin[location] = basin_number
            
            if basin_number is None:
                reverse_basin[location] = len(basins)
                basins.append(set([location]))

    for basin_number in range(len(basins)-1, -1, -1):
        merge_basins(basins, basin_number)

    return basins

def merge_basins(basins:List[Set[Point]], basin_number):
    for location in basins[basin_number]:
        for other_basin_number, other_basin in enumerate(basins):
            if other_basin_number != basin_number and location in other_basin:
                basins[other_basin_number].update(basins[basin_number])
                del basins[basin_number]
                return

def find_minima(heightmap: Dict[Point, int], size: Point) -> List[Point]:
    minima = []
    for y in range(size.y):
        for x in range(size.x):
            location = Point(x=x,y=y)
            if is_minimum(heightmap, location):
                minima.append(location)
    return minima

def previous_neighbors(location: Point):
    for x_delta, y_delta in [(0, -1), (-1,0)]:
        yield Point(location.x+x_delta, location.y+y_delta)

def neighbors(location: Point):
    for x_delta, y_delta in [(0,1), (0, -1), (1,0), (-1,0)]:
        yield Point(location.x+x_delta, location.y+y_delta)

def is_minimum(heightmap: Dict[Point, int], location: Point) -> bool:
    try:
        height = heightmap[location]
    except KeyError:
        return False

    for neighbor in neighbors(location):
        try:
            neighbor_height = heightmap[neighbor]
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

def basin_score(basins: List[Set[Point]]) -> int:
    return functools.reduce(operator.mul, sorted(len(b) for b in basins)[-3:])

def print_heightmap(heightmap: Dict[Point, int], size: Point, highlights: List[Point]):
    for y in range(size.y):
        for x in range(size.x):
            location = Point(x=x,y=y)
            if location in highlights:
                print('\033[1m', end='')
            print(heightmap[location], end='')
            if location in highlights:
                print('\033[0m', end='')
        print()

def generate_color_code(index: int):
    return u"\u001b[38;5;" + str(index) + "m"

def print_basins(heightmap: Dict[Point, int], size: Point, basins: List[Set[Point]]):
    def basin_index(location: Point) -> int:
        for i, basin in enumerate(basins):
            if location in basin:
                return 1+i
        return 0

    for y in range(size.y):
        for x in range(size.x):
            location = Point(x=y, y=x)
            print(generate_color_code(basin_index(location)), end='')
            print(u"\u2588", end='')
            print(u"\u001b[0m", end='')
        print()

heightmap, size = read_input(sys.stdin)
basins = find_basins(heightmap, size)
# score = risk_level(heightmap, minima)
# print_heightmap(heightmap, bounds, minima)

score = basin_score(basins)
print_basins(heightmap, size, basins)
print(score)