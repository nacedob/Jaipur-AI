# ai_player.py
import random
from typing import List, Dict
from ..market import Market
from ..deck import Deck, Card
from .base_player import BasePlayer

class AIPlayer(BasePlayer):
    def __init__(self, name: str = "AI") -> None:
        super().__init__(name)
        self.difficulty = 1  # 1: Easy, 2: Medium, 3: Hard

    def take_turn(self, market: Market, deck: Deck) -> bool:
        # Simple AI strategy - can be enhanced based on difficulty
        market_goods = market.goods()
        hand_goods = self.describe_hand()
        
        # Strategy 1: Sell if we have 3+ of any good
        for card, count in hand_goods.items():
            if card != Card.CAMEL and count >= 3:
                return self.sell_goods(card, count)
        
        # Strategy 2: Take camels if there are 3+ in market
        if len(market.camels()) >= 3:
            return self.take_camels(market, deck)
        
        # Strategy 3: Take a good that we already have 1-2 of
        for card in market_goods:
            if hand_goods.get(card, 0) >= 1 and hand_goods.get(card, 0) < 3:
                return self.take_single_good(card, market, deck)
        
        # Fallback: Take a random good
        if market_goods:
            card = random.choice(market_goods)
            return self.take_single_good(card, market, deck)
        
        # Last resort: Take camels if available
        if market.camels():
            return self.take_camels(market, deck)
        
        return False