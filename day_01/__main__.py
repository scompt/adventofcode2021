#!/usr/bin/env python

from typing import List
from utils import read_number_lines

def count_increases(numbers: List[int]):
    """
    >>> count_increases([0, 1, 2, 3])
    3
    >>> count_increases([0, 0, 0, 0])
    0
    """
    current = None
    count = 0

    for num in numbers:
        if current is not None and num > current:
            count += 1
        current = num
    return count

def make_windows(numbers: List[int], window_size:int = 3):
    for i in range(len(numbers)-window_size+1):
        yield numbers[i:i+window_size]

if __name__ == "__main__":
    import sys
    numbers = read_number_lines(sys.stdin)
    windows = make_windows(numbers, 3)
    numbers = [sum(window) for window in windows]
    increases = count_increases(numbers)
    print(increases)
