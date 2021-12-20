from typing import Generator, TextIO, List
import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int

    def neighbors(self) -> Generator["Point", None, None]:
        for y_delta in (-1,0,1):
            for x_delta in (-1,0,1):
                yield Point(x=self.x+x_delta, y=self.y+y_delta)

class Image:
    def __init__(self, algo):
        self.algo = algo
        self.points = set()
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    def set(self, point: Point, value: bool):
        if value:
            self.points.add(point)
            self.min_x = min(self.min_x, point.x)
            self.min_y = min(self.min_y, point.y)
            self.max_x = max(self.max_x, point.x)
            self.max_y = max(self.max_y, point.y)
        else:
            self.points.discard(point)

    def __len__(self):
        return len(self.points)

    def __str__(self):
        out = ''
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x, self.max_x+1):
                if Point(x,y) in self.points:
                    out += '#'
                else:
                    out += '.'
            out += '\n'
        out += f'{len(self)}\n'
        out += f'({self.max_y-self.min_y}, {self.max_x-self.min_x})'
        return out

    def _apply_algo(self, code: List[bool]):
        index = sum(1<<(8-index) for index, value in enumerate(code) if value)
        return self.algo[index] == '#'


    def step(self) -> "Image":
        extend = 10
        new_image = Image(self.algo)
        for y in range(self.min_y-extend, self.max_y+extend+1):
            for x in range(self.min_x-extend, self.max_x+extend+1):
                point = Point(x=x,y=y)
                code = [neighbor in self.points for neighbor in point.neighbors()]
                value = self._apply_algo(code)
                new_image.set(point, value)
                
        return new_image

def read_input(textio: TextIO):
    lines = textio.readlines()
    algo = lines[0].strip()

    image = Image(algo)
    image_input = lines[2:]
    for y, line in enumerate(image_input):
        for x, char in enumerate(line.strip()):
            image.set(Point(x,y), char == '#')
    return image

image = read_input(sys.stdin)


print(image)
print()
image = image.step()
print(image)
print()
image = image.step()
print(image)
print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
# print()
# image = image.step()
# print(image)
