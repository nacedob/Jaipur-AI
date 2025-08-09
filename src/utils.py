from icecream import ic
from typing import List, Tuple
from .deck import Card

SELL_BONUS = {3: 1, 4: 2, 5: 3}
BONUS_CAMEL = 5
GOODS_TOKEN_VALUES = {
    Card.DIAMOND: [7, 6, 5, 5, 4],
    Card.GOLD: [6, 5, 5, 4, 3],
    Card.SILVER: [5, 5, 4, 3, 2],
    Card.CLOTH: [5, 3, 3, 2, 1],
    Card.SPICE: [5, 3, 3, 2, 1],
    Card.LEATHER: [4, 3, 2, 1, 1]
}


def sell_tokens_for(goods_type: str, count: int) -> Tuple[List[int], int]:
    tokens = GOODS_TOKEN_VALUES[goods_type][:count]
    bonus = SELL_BONUS.get(count, 0)
    return tokens, bonus


def print_status(players: List['Player'], market: 'Market') -> None:
    print("\nMarket:", ', '.join(c.name for c in market.cards))
    for p in players:
        print(f"{p.name} hand: {p.describe_hand_str()}, Tokens: {sum(p.tokens)} points")
