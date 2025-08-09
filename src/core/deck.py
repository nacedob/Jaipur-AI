import random
from typing import List
from enum import Enum, auto


class Card(Enum):
    DIAMOND = auto()
    GOLD = auto()
    SILVER = auto()
    CLOTH = auto()
    SPICE = auto()
    LEATHER = auto()
    CAMEL = auto()


class Deck:
    def __init__(self) -> None:
        self.cards: List[str] = ([Card.CAMEL] * 11 +
                                 [Card.DIAMOND] * 6 +
                                 [Card.GOLD] * 6 +
                                 [Card.SILVER] * 6 +
                                 [Card.CLOTH] * 8 +
                                 [Card.SPICE] * 8 +
                                 [Card.LEATHER] * 10)
        random.shuffle(self.cards)

    def draw(self, n: int = 1) -> List[Card]:
        drawn = []
        for _ in range(n):
            if self.cards:
                drawn.append(self.cards.pop())
        return drawn

    def init_market(self) -> List[Card]:
        # Remove 3 camels from the market
        for _ in range(3):
            self.cards.remove(Card.CAMEL)

        # Take two random cards + 3 camels
        return self.draw(2) + [self.CAMEL] * 3