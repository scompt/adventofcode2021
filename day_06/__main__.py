from typing import TextIO, Dict
from collections import defaultdict
import sys

NEW_FISH_AGE=8
POST_REPRODUCTION_AGE=6

def step(input_state: Dict[int, int]) -> Dict[int, int]:
    output_state = defaultdict(lambda: 0)
    output_state[NEW_FISH_AGE] = input_state[0]
    output_state[POST_REPRODUCTION_AGE] = input_state[0]
    for i in range(1, NEW_FISH_AGE+1):
        output_state[i-1] += input_state[i]
    return output_state

def read_input(textio: TextIO) -> Dict[int, int]:
    state = defaultdict(lambda: 0)
    ages = [int(num) for num in textio.readlines()[0].split(',')]
    for age in ages:
        state[age] += 1
    return state

def print_state(state: Dict[int, int]):
    for i in range(NEW_FISH_AGE+1):
        print(f"{i}: {state[i]}")

state = read_input(sys.stdin)

for iteration in range(257):
    print(f"Iteration {iteration}")
    print("Count: %d" % sum(state.values()))
    print_state(state)
    state = step(state)
    print()