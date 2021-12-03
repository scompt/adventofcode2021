from utils import read_lines
import sys

BIT_COUNT=12

def asdf(numbers):
    gamma = 0
    epsilon = 0
    line_count = len(numbers)
    for bit in range(BIT_COUNT)[::-1]:
        one_count = 0
        for number in numbers:
            if number & (1<<bit):
                one_count += 1
        if one_count >= line_count/2:
            gamma += (1<<bit)

    for bit in range(BIT_COUNT):
        if gamma & (1<<bit) == 0:
            epsilon += (1<<bit)
    return gamma, epsilon
        
spec = {"bits": str}
numbers = [int(line['bits'], 2) for line in read_lines(sys.stdin, spec)]
gamma, epsilon = asdf(numbers)
print(gamma, epsilon, gamma * epsilon)
