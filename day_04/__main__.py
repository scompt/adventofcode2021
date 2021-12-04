from typing import Generator, Iterable, List, Set, TextIO, Tuple
import sys
import re
from itertools import chain

def chunks(lst, n):
    """Yield successive n-sized chunks from lst.
    
    https://stackoverflow.com/a/312464/111777
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Card:
    def __init__(self, numbers: List[int], card_size: int) -> None:
        self.numbers = numbers
        self.numbers_set = set(numbers)
        self.card_size = card_size
        self.marked_numbers = []
    
    def mark_number(self, number: int) -> None:
        self.marked_numbers.append(number)

    def is_winner(self) -> bool:
        marked_numbers = set(self.marked_numbers)
        for row_or_col in self._generate_rows_and_cols():
            if marked_numbers.issuperset(row_or_col):
                return True
        return False
    
    def _generate_rows_and_cols(self) -> Generator[Iterable[int], None, None]:
        # rows
        yield from chunks(self.numbers, self.card_size)
        
        # cols
        for start in range(self.card_size):
            yield [self.numbers[i] for i in range(start, self.card_size*self.card_size, self.card_size)]

    
    def score(self) -> int:
        return sum(self.numbers_set.difference(self.marked_numbers)) * self.marked_numbers[-1]
    
    def __repr__(self) -> str:
        out = "\n"
        for row in chunks(self.numbers, self.card_size):
            for num in row:
                out += str.format("{0: <3}", num)
            out += '\n'
        return out

def read_input(textio: TextIO, card_size: int) -> Tuple[List[int], List[Card]]:
    lines = textio.readlines()
    numbers = [int(n) for n in lines[0].strip().split(',')]
    cards = []

    for i in range(2, len(lines), card_size+1):
        card_lines = [re.split(' +', line.strip()) for line in lines[i:i+card_size]]
        card_numbers = [int(n) for n in chain.from_iterable(card_lines)]
        cards.append(Card(card_numbers, card_size))

    return numbers, cards

def play_bingo(numbers: List[int], cards:List[Card]):
    for number in numbers:
        for card in cards:
            card.mark_number(number)
            if card.is_winner():
                return card.score()
    raise Exception("No winner")
            
numbers, cards = read_input(sys.stdin, int(sys.argv[1]))
print(play_bingo(numbers, cards))