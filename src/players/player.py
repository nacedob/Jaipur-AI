from typing import List
from ..core.market import Market
from ..core.deck import Deck, Card
from ..core.utils import sell_tokens_for


class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: List[Card] = []
        self.camels: List[Card] = []
        self.tokens: List[int] = []

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
    
    def describe_hand(self) -> dict[Card, int]:
        d = dict.fromkeys(Card, 0)
        for c in self.hand:
            d[c] += 1
        d[Card.CAMEL] = len(self.camels)

    def take_single_good(self, card: Card, market: Market, deck: Deck) -> bool:
        # Check if movement is legal
        if card not in market.goods():
            print(f'No {card.name.lower()} in market. Available : {market.describe_str()}')
            return False

        # Replace card to market
        self.hand.append(card)
        market.remove_cards([card])
        market.add_cards(deck.draw())
        return True

    def take_camels(self, market: Market, deck: Deck) -> bool:
        camels_in_market = market.camels()
        if not camels_in_market:
            print("No camels to take in market.")
            return False
        self.camels.extend(camels_in_market)
        market.remove_cards(camels_in_market)
        market.add_cards(deck.draw(len(camels_in_market)))
        return True

    def sell_goods(self, card: Card, number: int) -> bool:
        hand_goods = set(self.hand)
        if not hand_goods:
            print("No goods to sell.")
            return False

        if card not in hand_goods or self.hand.count(card) < number:
            print(f"Invalid choice. Hand: {self.hand}")
            return False

        for _ in range(number):
            self.hand.remove(card)
        tokens, bonus = sell_tokens_for(card, number)
        self.tokens.extend(tokens)
        if bonus > 0:
            print(f"You get a sell bonus of {bonus} points!")
            self.tokens.append(bonus)
        return True

    def exchange(self, market: Market, take_dict: dict[Card], give_dict: dict[Card]) -> bool:
        
        # Assert take_dict and give_dict are not empty
        if not take_dict or give_dict:
            print('Please provide a not-empty take list and a give list.') 
            return False
            
        # Number of cards taken match the number of card given
        if sum(take_dict.values()) != sum(give_dict.values()):
            print(
                f'The number of cards taken ({sum(take_dict.values())}) does not match ' 
                + f'the number of cards to give ({sum(give_dict.values())})'
            )
        
        # Assert no exchanging camels
        if any(Card.CAMEL in take_dict):
            print("Invalid take list, cannot take camels here.")
            return False
        
        # Assert taken cards are in market
        market_goods = market.describe()
        if any(market_goods[c] < nb for c, nb in take_dict.items()):
            print(f"Some cards to give not in market. Market: {market.describe_str()}")
            return False
        
        # Assert given cards are in hand
        hand_goods = self.describe_hand()
        if any(hand_goods[c] < nb for c, nb in give_dict.items()):
                print(f"Some cards to give not in hand. Hand: {hand_goods}")
                return False
        
        # All passed. Perform trade
        for c, nb in take_dict.items():
            for _ in range(nb):
                self.hand.append(c)
                market.cards.remove(c)
        for c, nb in give_dict.items():
            for _ in range(nb):
                self.hand.remove(c)
                market.cards.append(c)
        return True