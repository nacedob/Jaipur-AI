# human_player.py
from typing import List, Dict, Optional
from ..market import Market
from ..deck import Deck, Card
from ...gui.basegui import BaseGUI
from .base_player import BasePlayer

class HumanPlayer(BasePlayer):
    def __init__(self, name: str, gui: BaseGUI) -> None:
        super().__init__(name)
        self.gui = gui

    def take_turn(self, market: Market, deck: Deck) -> bool:
        # Show turn options
        self.gui.show_turn_options()
        choice = self.gui.get_action_choice()

        # Handle action
        if choice == 1:
            goods_in_market = [card for card in market.goods() if market.cards.count(card) > 0]
            selected = self.gui.select_good(goods_in_market)
            if selected:
                return self.take_single_good(selected, market, deck)
        elif choice == 2:
            return self.take_camels(market, deck)
        elif choice == 3:
            player_goods = {card: self.hand.count(card) for card in Card if card != Card.CAMEL}
            selection = self.gui.select_goods_to_sell(player_goods)
            if selection:
                card, count = selection
                return self.sell_goods(card, count)
        elif choice == 4:
            self.gui.show_message("Exchange functionality not yet implemented")
        return False