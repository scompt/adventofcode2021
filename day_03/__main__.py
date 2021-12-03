from utils import read_lines
import sys

BIT_COUNT=int(sys.argv[1])

def count_bit_position(numbers, bit):
    count = 0
    for number in numbers:
        if number & 1<<bit:
            count += 1
    return count

def calculate_power_consumption(numbers):
    gamma = 0
    epsilon = 0
    line_count = len(numbers)
    for bit in range(BIT_COUNT)[::-1]:
        one_count = count_bit_position(numbers, bit)
        zeroes_count = line_count - one_count
        if one_count >= zeroes_count:
            gamma += (1<<bit)

    for bit in range(BIT_COUNT):
        if gamma & (1<<bit) == 0:
            epsilon += (1<<bit)
    return gamma, epsilon, gamma*epsilon

def calculate_life_support_rating(numbers):
    o2_candidates = list(numbers)
    co2_candidates = list(numbers)
    for bit in range(BIT_COUNT)[::-1]:
        if len(o2_candidates) > 1:
            ones = count_bit_position(o2_candidates, bit)
            zeroes = len(o2_candidates) - ones
            if ones >= zeroes:
                o2_candidates = [cand for cand in o2_candidates if cand & (1<<bit)]
            elif ones < zeroes:
                o2_candidates = [cand for cand in o2_candidates if not cand & (1<<bit)]

        if len(co2_candidates) > 1:
            ones = count_bit_position(co2_candidates, bit)
            zeroes = len(co2_candidates) - ones
            if ones < zeroes:
                co2_candidates = [cand for cand in co2_candidates if cand & (1<<bit)]
            elif ones >= zeroes:
                co2_candidates = [cand for cand in co2_candidates if not cand & (1<<bit)]
    return o2_candidates[0], co2_candidates[0], o2_candidates[0] * co2_candidates[0]


spec = {"bits": str}
numbers = [int(line['bits'], 2) for line in read_lines(sys.stdin, spec)]
_, _, power_consumption = calculate_power_consumption(numbers)
print(power_consumption)
_, _, life_support_rating = calculate_life_support_rating(numbers)
print(life_support_rating)
