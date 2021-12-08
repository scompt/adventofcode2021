from typing import TextIO, List
import sys

def read_input(textio: TextIO) -> List[int]:
    count = 0
    for line in textio.readlines():
        before, after = line.strip().split(' | ')
        for word in after.split(' '):
            print(word)
            if len(word) in (2, 3, 4, 7):
                print('*')
                count += 1
    print(count)



read_input(sys.stdin)