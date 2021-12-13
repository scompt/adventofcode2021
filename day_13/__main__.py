from typing import TextIO, Set
import sys
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])
Fold = namedtuple("Fold", ['axis', 'value'])

def read_input(textio: TextIO):
    dots = set()
    folds = []
    max_x = max_y = 0
    
    lines = textio.readlines()
    for i, line in enumerate(lines):
        if line.strip():
            loc = Point(*(int(value) for value in line.strip().split(',')))
            max_x = max(max_x, loc.x)
            max_y = max(max_y, loc.y)
            dots.add(loc)
        else:
            break
    
    for line in lines[i+1:]:
        axis, value = line[11:-1].split('=')
        fold = Fold(axis, int(value))
        folds.append(fold)

    return dots, folds, Point(x=max_x+1, y=max_y+1)

def print_transparency(dots, size, fold=None):
    for y in range(size.y):
        if fold and fold.axis == 'y' and fold.value == y:
            print('-'*size.x)
            continue

        for x in range(size.x):
            if fold and fold.axis == 'x' and fold.value == x:
                print('|', end='')
            elif Point(x=x,y=y) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print()

def extract_dots(dots, from_loc: Point, to_loc: Point):
    out_dots = set()
    for y in range(from_loc.y, to_loc.y):
        for x in range(from_loc.x, to_loc.x):
            loc = Point(x=x, y=y)
            if loc in dots:
                out_dots.add(loc)
    return out_dots


def make_fold(dots, size, fold):
    if fold.axis == 'y':
        new_size = Point(x=size.x, y=size.y//2)
        new_dots = extract_dots(dots, Point(0,0), new_size)
        fold_dots = extract_dots(dots, Point(x=0, y=size.y//2), size)
        fold_dots = flip_dots(fold_dots, fold_y=fold.value)

    elif fold.axis == 'x':
        new_size = Point(x=size.x//2, y=size.y)
        new_dots = extract_dots(dots, Point(0,0), new_size)
        fold_dots = extract_dots(dots, Point(x=size.x//2, y=0), size)
        fold_dots = flip_dots(fold_dots, fold_x=fold.value)

    return fold_dots.union(new_dots), new_size

def flip_dots(dots: Set[Point], fold_x:int=None, fold_y:int=None):
    out_dots = set()
    for dot in dots:
        if fold_x is not None:
            new_dot = Point(x=2*fold_x-dot.x, y=dot.y)
        elif fold_y is not None:
            new_dot = Point(x=dot.x, y=2*fold_y-dot.y)
        out_dots.add(new_dot)
    return out_dots
        

dots, folds, size = read_input(sys.stdin)
dots, size = make_fold(dots, size, folds[0])

print(len(dots))

for fold in folds[1:]:
    dots, size = make_fold(dots, size, fold)

print_transparency(dots, size)