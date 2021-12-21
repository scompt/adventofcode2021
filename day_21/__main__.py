from collections import defaultdict
from typing import TextIO, List, Generator, Tuple
import sys
import itertools
from functools import cache
from dataclasses import dataclass

TARGET_SCORE = 21
NUM_POSITIONS = 10
ROLLS_PER_TURN = 3
DIE_SIZE=3

ROLLS = [sum(rolls) for rolls in list(itertools.product(range(1,DIE_SIZE+1), repeat=ROLLS_PER_TURN))]

@dataclass(frozen=True, eq=True)
class GameState:
    positions: Tuple[int]
    scores: Tuple[int]=(0,0)
    player_turn: int=0

    def is_winner(self) -> bool:
        return any(score>=TARGET_SCORE for score in self.scores)
    
    def get_winner(self) -> int:
        winning_score = next(filter(lambda score: score >= TARGET_SCORE, self.scores))
        return self.scores.index(winning_score)
    
    def next_turns(self) -> Generator["GameState", None, None]:
        next_player_turn = (self.player_turn+1)%2
        for roll in ROLLS:
            next_scores = list(self.scores)
            next_positions = list(self.positions)
            next_positions[self.player_turn] = (next_positions[self.player_turn] - 1 + roll) % NUM_POSITIONS + 1
            next_scores[self.player_turn] += next_positions[self.player_turn]
            yield GameState(positions=tuple(next_positions), scores=tuple(next_scores), player_turn=next_player_turn)

def read_input(textio:TextIO):
    lines = textio.readlines()
    player_1 = int(lines[0][-2:-1])
    player_2 = int(lines[1][-2:-1])
    return GameState(positions=(player_1, player_2))

@cache
def traverse(state) -> Tuple[int, int]:
    winners = [0, 0]
    if state.is_winner():
        winners[state.get_winner()] += 1

    else:
        for child in state.next_turns():
            child_winners = traverse(child)
            winners[0] += child_winners[0]
            winners[1] += child_winners[1]

    return tuple(winners)

state = read_input(sys.stdin)
winners = traverse(state)
print(max(winners))