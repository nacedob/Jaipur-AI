from typing import List
from .deck import Deck, Card


class Market:
    def __init__(self, deck: Deck) -> None:
        self.cards: List[Card] = [Card.CAMEL, Card.CAMEL, Card.CAMEL] + deck.draw(2)

    def add_cards(self, cards: List[Card]) -> None:
        self.cards.extend(cards)

    def remove_cards(self, cards_to_remove: List[Card]) -> None:
        for c in cards_to_remove:
            self.cards.remove(c)

    def camels(self) -> List[Card]:
        return [c for c in self.cards if c == Card.CAMEL]

    def goods(self) -> List[Card]:
        return [c for c in self.cards if c != Card.CAMEL]

    def describe_str(self) -> str:
        return (
            '| '.join(c.name.capitalize() for c in self.goods) + f'Camels: {len(self.camels)}'
        )
        
    def describe(self) -> dict[Card, int]:
        d = dict.fromkeys(Card, 0)
        for g in self.cards:
            d[g] += 1
        return d
        