from typing import Generator, TextIO, Dict
import sys
from collections import namedtuple
import time

Point = namedtuple("Point", ['x', 'y'])

COLORS = [(237, 245, 255), (208, 226, 255), (166, 200, 255), (120, 169, 255), (69, 137, 255), (15, 98, 254), (0, 67, 206), (0, 45, 156), (0, 29, 108), (0, 17, 65)]

class Cavern:
    @staticmethod
    def read_input(textio: TextIO) -> "Cavern":
        output = dict()
        lines = textio.readlines()
        for y, line in enumerate(lines):
            line = line.strip()
            for x, height in enumerate(line):
                output[Point(x=x,y=y)] = int(height)
        return Cavern(output, Point(x=len(line), y=len(lines)))

    def __init__(self, octopi: Dict[Point, int], size: Point):
        self.octopi = octopi
        self.size = size
        self.flash_count = 0

    def step(self):
        for point in self._points():
            self.octopi[point] += 1
        
        while True:
            flashes = set()
            for point in self._points():
                if self.octopi[point] > 9:
                    flashes.add(point)
                    self.octopi[point] = 0
            
            for flash in flashes:
                for neighbor in self._neighbors(flash):
                    if self.octopi[neighbor] > 0:
                        self.octopi[neighbor] += 1
            
            self.flash_count += len(flashes)
            if not flashes:
                break
        
        total_energy = sum(self.octopi[loc] for loc in self._points())
        return total_energy == 0
    
    def _neighbors(self, location: Point):
        for x_delta in [-1, 0, 1]:
            for y_delta in [-1, 0, 1]:
                if x_delta or y_delta:
                    x = location.x+x_delta
                    y = location.y+y_delta
                    if x>=0 and y>=0 and x<self.size.x and y<self.size.y:
                        yield Point(x=location.x+x_delta, y=location.y+y_delta)

    def __str__(self):
        output = ""
        for y in range(self.size.y):
            for x in range(self.size.x):
                location = Point(x=x, y=y)
                energy = self.octopi[location]
                output += '\033['
                # if energy == 0:
                #     output += '1;'
                color = COLORS[energy]
                output += f'38;2;{color[0]};{color[1]};{color[2]}m' 
                # output += str(self.octopi[location])
                output += u"\u2588"
                output += '\033[0m'
            output += '\n'
        return output

    def _points(self) -> Generator[Point, None, None]:
        for y in range(self.size.y):
            for x in range(self.size.x):
                yield Point(x=x,y=y)

cavern = Cavern.read_input(sys.stdin)
step = 0
while True:
    time.sleep(2/60)
    sync = cavern.step()
    print('\033[H')
    print(cavern)
    step += 1
    if sync:
        print(f"Synced on step {step}")
        break
