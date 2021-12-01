from typing import TextIO, List

def read_number_lines(textio: TextIO) -> List[int]:
    lines = textio.readlines()
    return [int(line) for line in lines]