from typing import TextIO, List
import sys

def read_input(textio: TextIO) -> List[int]:
    positions = [int(num) for num in textio.readlines()[0].split(',')]
    return positions

def cost(position: int, target_position: int) -> int:
    diff = abs(position-target_position)
    return int((diff+1)*diff/2)

def total_cost(positions:List[int], target_position:int) -> int:
    return sum(cost(position, target_position) for position in positions)

def find_cheapest(positions:List[int]):
    min_pos = min(positions)
    max_pos = max(positions)

    costs = dict()
    for pos in range(min_pos, max_pos+1):
        costs[pos] = total_cost(positions, pos)

    min_cost_pos = min(costs, key=costs.get)
    return min_cost_pos, costs[min_cost_pos]

positions = read_input(sys.stdin)
print(find_cheapest(positions))
