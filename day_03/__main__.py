from utils import read_lines
import sys

BIT_COUNT=12

def count_bit_position(numbers, bit):
    count = 0
    for number in numbers:
        if number & 1<<bit:
            count += 1
    return count

def asdf(numbers):
    gamma = 0
    epsilon = 0
    omega = 0
    line_count = len(numbers)
    for bit in range(BIT_COUNT)[::-1]:
        one_count = 0
        for number in numbers:
            if number & (1<<bit):
                one_count += 1
        if one_count > line_count/2:
            gamma += (1<<bit)
        elif one_count == line_count / 2:
            omega += (1<<bit)

    for bit in range(BIT_COUNT):
        if gamma & (1<<bit) == 0:
            epsilon += (1<<bit)
    return gamma, epsilon, omega

def qwer(numbers):
    life_support_rating = 1
    gamma, epsilon, omega = asdf(numbers)
    print(bin(omega))
    o2_candidates = list(numbers)
    co2_candidates = list(numbers)
    for bit in range(BIT_COUNT)[::-1]:
        print(bit, [bin(c) for c in o2_candidates])
        ones = count_bit_position(o2_candidates, bit)
        zeroes = len(o2_candidates) - ones
        print(ones, zeroes)
        if ones >= zeroes:
            o2_candidates = [cand for cand in o2_candidates if cand & (1<<bit)]
        elif ones < zeroes:
            o2_candidates = [cand for cand in o2_candidates if not cand & (1<<bit)]
        if len(o2_candidates) == 1:
            life_support_rating = life_support_rating * o2_candidates[0]
            print('o2', o2_candidates[0])
        
        ones = count_bit_position(co2_candidates, bit)
        zeroes = len(co2_candidates) - ones
        print(ones, zeroes)
        if ones < zeroes:
            co2_candidates = [cand for cand in co2_candidates if cand & (1<<bit)]
        elif ones >= zeroes:
            co2_candidates = [cand for cand in co2_candidates if not cand & (1<<bit)]
        if len(co2_candidates) == 1:
            life_support_rating = life_support_rating * co2_candidates[0]
            print('co2', co2_candidates[0])
        print(life_support_rating)



spec = {"bits": str}
numbers = [int(line['bits'], 2) for line in read_lines(sys.stdin, spec)]
gamma, epsilon, omega = asdf(numbers)
# print(gamma, epsilon, gamma * epsilon)
qwer(numbers)
