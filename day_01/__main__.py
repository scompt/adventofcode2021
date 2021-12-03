from typing import List
from utils import read_lines
import sys

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

lines = read_lines(sys.stdin, {"number": int})
numbers = [line['number'] for line in lines]
windows = make_windows(numbers, 3)
numbers = [sum(window) for window in windows]
increases = count_increases(numbers)
print(increases)
