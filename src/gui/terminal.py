# gui.py
from typing import List, Dict, Optional
from ..core import Card
from .base import BaseGUI
from .views import PlayerView, MarketView
from colorama import init, Fore, Back, Style
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)

class TerminalGUI(BaseGUI):
    # Card emoji mapping
    CARD_EMOJIS = {
        Card.DIAMOND: "💎",
        Card.GOLD: "🪙",
        Card.SILVER: "⚪",
        Card.CLOTH: "🧵",
        Card.SPICE: "🍛",
        Card.LEATHER: "🟫",
        Card.CAMEL: "🐫"
    }

    # Card colors
    CARD_COLORS = {
        Card.DIAMOND: Fore.CYAN,
        Card.GOLD: Fore.YELLOW,
        Card.SILVER: Fore.WHITE,
        Card.CLOTH: Fore.LIGHTWHITE_EX,
        Card.SPICE: Fore.RED,
        Card.LEATHER: Fore.LIGHTYELLOW_EX,
        Card.CAMEL: Fore.LIGHTYELLOW_EX
    }

    @staticmethod
    def clear_screen():
        print("\033c", end="")  # ANSI escape code to clear terminal

    def _format_card(self, card: Card, count: int = 1) -> str:
        """Format a card with emoji and color"""
        color = self.CARD_COLORS.get(card, Fore.WHITE)
        return f"{color}{self.CARD_EMOJIS[card]} {card.name}{Style.RESET_ALL} ×{count}"

    def show_game_state(self, players: List[PlayerView], market: MarketView, current_player_name: str = None):
        self.clear_screen()
        
        # Header with turn indicator
        print(Fore.GREEN + "=== JAIPUR ===" + Style.RESET_ALL)
        print("==========================")

        # Market display
        market_table = []
        for card, count in market.goods.items():
            if count > 0:
                market_table.append([self._format_card(card), count])
        if market.camels > 0:
            market_table.append([self._format_card(Card.CAMEL), market.camels])
        
        print(Fore.BLUE + "\nMARKET:" + Style.RESET_ALL)
        if market_table:
            print(tabulate(market_table, 
                         headers=["Card", "Count"], 
                         tablefmt="grid",
                         numalign="center",
                         stralign="left"))
        else:
            print("  Empty")

        # Players display
        print(Fore.CYAN + "\nPLAYERS:" + Style.RESET_ALL)
        players_table = []
        
        for player in players:
            is_current = player.name == current_player_name
            player_color = Fore.GREEN if is_current else Fore.BLUE
            
            # Hand information - combine all cards into one cell
            if is_current:
                hand_items = [
                    f"{self._format_card(card, count)}"
                    for card, count in player.hand.items() 
                    if count > 0
                ]
                hand_info = "\n".join(hand_items) if hand_items else "Empty"
            else:
                total_cards = sum(player.hand.values())
                hand_info = f"{Fore.LIGHTBLACK_EX}{total_cards} hidden cards{Style.RESET_ALL}"
            
            players_table.append([
                player_color + player.name + Style.RESET_ALL,
                hand_info,
                self._format_card(Card.CAMEL, player.camels),
                f"{Fore.YELLOW}{player.tokens} points{Style.RESET_ALL}"
            ])
        
        if current_player_name:
            print(Fore.MAGENTA + f"=== {current_player_name}'s Turn ===" + Style.RESET_ALL)
            
        print(tabulate(players_table,
                      headers=["Player", "Hand", "Camels", "Tokens"],
                      tablefmt="grid",
                      numalign="center",
                      stralign="left"))
    
    def show_turn_options(self):
        options = [
            ["1", "✋ Take single good from market"],
            ["2", "🐫 Take all camels from market"],
            ["3", "💰 Sell goods"],
            ["4", "🔄 Exchange cards"],
            ["5", "👀 View game state"]
        ]
        
        print(Fore.CYAN + "\n🎮 Choose action:" + Style.RESET_ALL)
        print(tabulate(options,
                      tablefmt="simple",
                      colalign=("center", "left")))

    def get_action_choice(self) -> int:
        while True:
            try:
                choice = input(Fore.CYAN + "\nEnter action (1-5): " + Style.RESET_ALL).strip()
                if choice.isdigit():
                    choice_int = int(choice)
                    if 1 <= choice_int <= 5:
                        return choice_int
                print(Fore.RED + "Please enter a number between 1 and 5" + Style.RESET_ALL)
            except KeyboardInterrupt:
                raise
            except:
                print(Fore.RED + "Invalid input" + Style.RESET_ALL)

    def select_good(self, available_goods: List[Card]) -> Optional[Card]:
        print(Fore.CYAN + "\n🛍️ Available goods:" + Style.RESET_ALL)
        for i, card in enumerate(available_goods, 1):
            print(f"{Fore.YELLOW}{i}){Style.RESET_ALL} {self._format_card(card)}")
        print(f"{Fore.YELLOW}0){Style.RESET_ALL} Cancel")

        try:
            choice = input(Fore.CYAN + "\nSelect good: " + Style.RESET_ALL).strip()
            if choice == "0":
                return None
            if choice.isdigit():
                choice_int = int(choice)
                if 1 <= choice_int <= len(available_goods):
                    return available_goods[choice_int - 1]
            print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
        except KeyboardInterrupt:
            raise
        except:
            print(Fore.RED + "Please enter a valid number" + Style.RESET_ALL)
        return None

    def select_goods_to_sell(self, player_goods: Dict[Card, int]) -> Optional[tuple[Card, int]]:
        print(Fore.CYAN + "\n💰 Your goods:" + Style.RESET_ALL)
        goods_list = [card for card, count in player_goods.items() if count > 0]

        for i, card in enumerate(goods_list, 1):
            print(f"{Fore.YELLOW}{i}){Style.RESET_ALL} {self._format_card(card, player_goods[card])}")
        print(f"{Fore.YELLOW}0){Style.RESET_ALL} Cancel")

        try:
            card_choice = input(Fore.CYAN + "\nSelect good to sell: " + Style.RESET_ALL).strip()
            if card_choice == "0":
                return None
            if card_choice.isdigit():
                card_choice_int = int(card_choice)
                if 1 <= card_choice_int <= len(goods_list):
                    card = goods_list[card_choice_int - 1]
                    max_count = player_goods[card]
                    count = input(
                        Fore.CYAN + f"How many to sell (1-{max_count}): " + Style.RESET_ALL
                    ).strip()
                    if count.isdigit():
                        count_int = int(count)
                        if 1 <= count_int <= max_count:
                            return (card, count_int)
            print(Fore.RED + "Invalid selection" + Style.RESET_ALL)
        except KeyboardInterrupt:
            raise
        except:
            print(Fore.RED + "Please enter valid numbers" + Style.RESET_ALL)
        return None

    def show_message(self, message: str):
        print(Fore.GREEN + "\n📢 " + message + Style.RESET_ALL)
        input(Fore.CYAN + "Press Enter to continue..." + Style.RESET_ALL)

    def show_error(self, error: str):
        print(Fore.RED + "\n❌ ERROR: " + error + Style.RESET_ALL)
        input(Fore.CYAN + "Press Enter to continue..." + Style.RESET_ALL)