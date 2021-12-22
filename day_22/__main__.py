from typing import TextIO, List
import sys
from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int
    z: int

@dataclass(frozen=True, eq=True)
class Instruction:
    action: bool
    from_point: Point
    to_point: Point

def flatten(t):
    return [item for sublist in t for item in sublist]

def read_input(textio: TextIO):
    instructions = []
    for line in textio.readlines():
        action, loc = line.strip().split(' ')
        dims = [int(dim) for dim in flatten([dim.split('..') for dim in [dim[2:] for dim in loc.split(',')]])]
        instructions.append(Instruction(action=='on', Point(dims[0], dims[2], dims[4]), Point(dims[1], dims[3], dims[5])))
    return instructions

def apply_instructions(instructions: List[Instruction]):
    reactor = set()
    for instruction in instructions:
        if instruction.action:
            func = set.add
        else:
            func = set.discard
        
        for x in range(max(-50, instruction.from_point.x), min(50, instruction.to_point.x)+1):
            for y in range(max(-50, instruction.from_point.y), min(50, instruction.to_point.y)+1):
                for z in range(max(-50, instruction.from_point.z), min(50, instruction.to_point.z)+1):
                    func(reactor, Point(x=x,y=y,z=z))
    return reactor

instructions = read_input(sys.stdin)
reactor = apply_instructions(instructions)
print(len(reactor))