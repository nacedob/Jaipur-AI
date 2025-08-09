# gui.py
from typing import List, Dict, Optional
from dataclasses import dataclass
from ..deck import Card
from .base import BaseGUI, BasePlayerView, BaseMarketView


@dataclass
class TerminalPlayerView(BasePlayerView):
    name: str
    hand: Dict[Card, int]
    camels: int
    tokens: int


@dataclass
class TerminalMarketView(BaseMarketView):
    goods: Dict[Card, int]
    camels: int


class TerminalGUI(BaseGUI):
    @staticmethod
    def clear_screen():
        print("\033c", end="")  # ANSI escape code to clear terminal

    def show_game_state(self, players: List[TerminalPlayerView], market: TerminalMarketView):
        self.clear_screen()
        print("=== JAIPUR ===")
        print("==============")
        
        # Show market
        print("\nMARKET:")
        for card, count in market.goods.items():
            print(f"  {card.name}: {count}")
        print(f"  CAMELS: {market.camels}")

        # Show players
        for player in players:
            print(f"\n{player.name}:")
            print("  HAND:")
            for card, count in player.hand.items():
                if count > 0:
                    print(f"    {card.name}: {count}")
            print(f"  CAMELS: {player.camels}")
            print(f"  TOKENS: {player.tokens} points")

    def show_turn_options(self):
        print("\nChoose action:")
        print("1) Take single good from market")
        print("2) Take all camels from market")
        print("3) Sell goods")
        print("4) Exchange cards")
        print("5) View game state")

    def get_action_choice(self) -> int:
        while True:
            try:
                choice = int(input("Enter action (1-5): "))
                if 1 <= choice <= 5:
                    return choice
                print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")

    def select_good(self, available_goods: List[Card]) -> Optional[Card]:
        print("\nAvailable goods:")
        for i, card in enumerate(available_goods, 1):
            print(f"{i}) {card.name}")
        print("0) Cancel")

        try:
            choice = int(input("Select good: "))
            if choice == 0:
                return None
            if 1 <= choice <= len(available_goods):
                return available_goods[choice - 1]
            print("Invalid selection")
        except ValueError:
            print("Please enter a number")
        return None

    def select_goods_to_sell(self, player_goods: Dict[Card, int]) -> Optional[tuple[Card, int]]:
        print("\nYour goods:")
        goods_list = [card for card, count in player_goods.items() if count > 0]

        for i, card in enumerate(goods_list, 1):
            print(f"{i}) {card.name}: {player_goods[card]}")
        print("0) Cancel")

        try:
            card_choice = int(input("Select good to sell: "))
            if card_choice == 0:
                return None
            if 1 <= card_choice <= len(goods_list):
                card = goods_list[card_choice - 1]
                max_count = player_goods[card]
                count = int(input(f"How many to sell (1-{max_count}): "))
                if 1 <= count <= max_count:
                    return (card, count)
                print("Invalid quantity")
            else:
                print("Invalid selection")
        except ValueError:
            print("Please enter numbers")
        return None

    def show_message(self, message: str):
        print(f"\n{message}")
        input("Press Enter to continue...")

    def show_error(self, error: str):
        print(f"\nERROR: {error}")
        input("Press Enter to continue...")
