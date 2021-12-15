from typing import TextIO, Dict, List, Optional, Tuple
from collections import namedtuple, defaultdict
import sys

Point = namedtuple("Point", ['x', 'y'])

def read_input(textio: TextIO):
    cave = dict()
    max_x = max_y = 0
    
    lines = textio.readlines()
    for y, line in enumerate(lines):
        for x, value in enumerate(int(value) for value in line.strip()):
            loc = Point(x=x, y=y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            cave[loc] = value
    
    return cave, Point(x=max_x+1, y=max_y+1)

def neighbors(location: Point, size: Point):
    for x_delta, y_delta in [(0,1), (0, -1), (1,0), (-1,0)]:
        x = location.x+x_delta
        y = location.y+y_delta

        if x>=0 and y>=0 and x<size.x and y<size.y:
            yield Point(x=x, y=y), location

def visit(cave: Dict[Point, int], size: Point) -> Dict[Point, Tuple[int, Optional[Point]]]:
    visited = {Point(0,0):(0, None)}
    to_visit = list(neighbors(Point(0,0), size))

    while len(to_visit) > 0:
        node_to, node_from = to_visit.pop(0)
        new_cost = visited[node_from][0]+cave[node_to]
        if node_to in visited:
            if new_cost < visited[node_to][0]:
                visited[node_to] = (new_cost, node_from)
                to_visit.extend(neighbors(node_to, size))
            else:
                pass
        else:
            visited[node_to] = (new_cost, node_from)
            to_visit.extend(neighbors(node_to, size))
    return visited
    
def find_path(cave: Dict[Point, int], costs: Dict[Point, Tuple[int, Optional[Point]]], finish: Point):
    path = []
    node = finish
    while node:
        path.append(node)
        node = costs[node][1]

    return path

def print_cave(cave: Dict[Point, int], size: Point, path: List[Point]):
    for y in range(size.y):
        for x in range(size.x):
            location = Point(x=x,y=y)
            if location in path:
                print('\033[1m', end='')
            print(cave[location], end='')
            print('\033[0m', end='')
        print()
    print()

cave, size = read_input(sys.stdin)

start = Point(x=0, y=0)
finish = Point(x=size.x-1,y=size.y-1)
visits = visit(cave, size)

path = find_path(cave, visits, finish)
print_cave(cave, size, path)
print(visits[finish][0])