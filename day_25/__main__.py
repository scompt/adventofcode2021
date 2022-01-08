from typing import TextIO, Dict, List, Set
import sys
from collections import defaultdict
import enum
from dataclasses import dataclass



class CucumberDirection(enum.Enum):
    DOWN = 'v',
    RIGHT = '>'

@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


class World:
    @staticmethod
    def read_input(textio: TextIO):
        max_x = max_y = 0
        seafloor = dict()
        cukes = defaultdict(lambda: set())
        for y, line in enumerate(textio.readlines()):
            max_y = max(max_y, y)
            for x, c in enumerate(line.strip()):
                max_x = max(max_x, x)
                loc = Point(x,y)
                match c:
                    case 'v':
                        cuke_dir = CucumberDirection.DOWN
                    case '>':
                        cuke_dir = CucumberDirection.RIGHT
                    case _:
                        continue
                seafloor[loc] = cuke_dir
                cukes[cuke_dir].add(loc)
        return World(seafloor, Point(max_x+1, max_y+1), cukes)
    
    def __init__(self, seafloor: Dict[Point, CucumberDirection], size: Point, cukes: Dict[CucumberDirection, Set[Point]]):
        self.seafloor = seafloor
        self.size = size
        self.cukes = cukes
    
    def __str__(self):
        out = ''
        for y in range(self.size.y):
            for x in range(self.size.x):
                loc = Point(x,y)
                if loc in self.seafloor:
                    out += self.seafloor[loc].value[0]
                else:
                    out += '.'
            out += '\n'
        return out[:-1]
    
    def _next_loc(self, cuke: Point, direction: CucumberDirection):
        match direction:
            case CucumberDirection.DOWN:
                x = cuke.x
                y = (cuke.y + 1) % self.size.y

            case CucumberDirection.RIGHT:
                x = (cuke.x + 1) % self.size.x
                y = cuke.y

        return Point(x,y)

    def step(self):
        something_moved = False
        for direction in [CucumberDirection.RIGHT, CucumberDirection.DOWN]:
            movers = []
            for cuke in self.cukes[direction]:
                next_loc = self._next_loc(cuke, direction)
                if next_loc not in self.seafloor:
                    movers.append((cuke, next_loc))
            
            for from_loc, to_loc in movers:
                something_moved = True
                del self.seafloor[from_loc]
                self.seafloor[to_loc] = direction
                self.cukes[direction].remove(from_loc)
                self.cukes[direction].add(to_loc)
            print(len(movers))
        return something_moved


world = World.read_input(sys.stdin)
step = 0
while True:
    # print("\033c", end="")
    # print(world)
    print(step)
    # print()
    something_moved = world.step()
    step += 1

    if not something_moved:
        print(f'Stopped moving after {step} steps')
        break

