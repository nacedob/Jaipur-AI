# player.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..market import Market
from ..deck import Deck, Card
from ..utils import sell_tokens_for

class BasePlayer(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: List[Card] = []
        self.camels: List[Card] = []
        self.tokens: List[int] = []
        self.transactions: Dict[Card, int] = {card: 0 for card in Card}

    def add_cards_to_hand(self, cards: List[Card]) -> None:
        camels = [c for c in cards if c == Card.CAMEL]
        goods = [c for c in cards if c != Card.CAMEL]
        self.camels.extend(camels)
        self.hand.extend(goods)

    def describe_hand_str(self) -> str:
        hand_str = ''
        for c in Card:
            c_name = c.name.capitalize()
            hand_str += f'{c_name}: {self.hand.count(c)} |'
        return hand_str + f' Camels: {len(self.camels)}'
    
    def describe_hand(self) -> Dict[Card, int]:
        d = {card: 0 for card in Card}
        for c in self.hand:
            d[c] += 1
        d[Card.CAMEL] = len(self.camels)
        return d

    @abstractmethod
    def take_turn(self, market: Market, deck: Deck) -> bool:
        pass

    def take_single_good(self, card: Card, market: Market, deck: Deck) -> bool:
        if card not in market.goods():
            return False
        self.hand.append(card)
        market.remove_cards([card])
        market.add_cards(deck.draw())
        return True

    def take_camels(self, market: Market, deck: Deck) -> bool:
        camels_in_market = market.camels()
        if not camels_in_market:
            return False
        self.camels.extend(camels_in_market)
        market.remove_cards(camels_in_market)
        market.add_cards(deck.draw(len(camels_in_market)))
        return True

    def sell_goods(self, card: Card, number: int) -> bool:
        if card not in self.hand or self.hand.count(card) < number:
            return False
        for _ in range(number):
            self.hand.remove(card)
        tokens, bonus = sell_tokens_for(card, number)
        self.tokens.extend(tokens)
        if bonus > 0:
            self.tokens.append(bonus)
        self.transactions[card] += number
        return True

    def exchange(self, market: Market, take_dict: Dict[Card, int], give_dict: Dict[Card, int]) -> bool:
        if not take_dict or not give_dict:
            return False
        if sum(take_dict.values()) != sum(give_dict.values()):
            return False
        if any(c == Card.CAMEL for c in take_dict):
            return False
            
        market_goods = {card: market.cards.count(card) for card in Card}
        if any(market_goods[c] < nb for c, nb in take_dict.items()):
            return False
            
        hand_goods = self.describe_hand()
        if any(hand_goods[c] < nb for c, nb in give_dict.items()):
            return False
            
        for c, nb in take_dict.items():
            for _ in range(nb):
                self.hand.append(c)
                market.cards.remove(c)
        for c, nb in give_dict.items():
            for _ in range(nb):
                self.hand.remove(c)
                market.cards.append(c)
        return True