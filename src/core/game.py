from typing import List
from collections import defaultdict
from .market import Market
from ..players.player import Player
from .deck import Deck, Card
from ..gui import (TerminalGUI,
                  PygameGUI,
                  BaseGUI, PlayerView, MarketView)


class Game:
    def __init__(self, gui: str = 'terminal') -> None:
        self.deck = Deck()
        self.market = Market(self.deck)
        self.players: List[Player] = [Player("Player 1"), Player("Player 2")]
        self.gui: BaseGUI = TerminalGUI() if gui == 'terminal' else PygameGUI()
        self.transactions = {card: 0 for card in Card}

        for p in self.players:
            initial = self.deck.draw(5)
            p.add_cards_to_hand(initial)
        self.turn = 0

    def get_player_view(self, player: Player) -> PlayerView:
        hand_counts = {card: player.hand.count(card) for card in Card}
        return PlayerView(
            name=player.name,
            hand=hand_counts,
            camels=len(player.camels),
            tokens=sum(player.tokens)
        )

    def get_market_view(self) -> MarketView:
        goods_counts = {card: self.market.cards.count(card) for card in Card if card != Card.CAMEL}
        return MarketView(
            goods=goods_counts,
            camels=self.market.cards.count(Card.CAMEL)
        )

    def is_game_over(self) -> bool:
        return len(self.deck.cards) == 0 or sum(v == 5 for v in self.transactions.values()) >= 3

    def play_turn(self) -> None:
        current_player = self.players[self.turn % 2]

        # Show game state
        players_view = [self.get_player_view(p) for p in self.players]
        market_view = self.get_market_view()
        self.gui.show_game_state(players_view, market_view, current_player.name)

        # Get player action
        self.gui.show_turn_options()
        choice = self.gui.get_action_choice()

        # Handle action
        success = False
        if choice == 1:
            goods_in_market = [card for card in self.market.goods() if self.market.cards.count(card) > 0]
            selected = self.gui.select_good(goods_in_market)
            if selected:
                success = current_player.take_single_good(selected, self.market, self.deck)
        elif choice == 2:
            success = current_player.take_camels(self.market, self.deck)
        elif choice == 3:
            player_goods = {card: current_player.hand.count(card) for card in Card if card != Card.CAMEL}
            selection = self.gui.select_goods_to_sell(player_goods)
            if selection:
                card, count = selection
                success = current_player.sell_goods(card, count)
                if success:
                    self.transactions[card] += count
        elif choice == 4:
            self.gui.show_message("Exchange functionality not yet implemented")
        elif choice == 5:
            # Just show state again
            success = False

        if success:
            self.turn += 1

    def final_scoring(self) -> None:
        players_view = [self.get_player_view(p) for p in self.players]
        market_view = self.get_market_view()
        self.gui.show_game_state(players_view, market_view)

        print("\nFinal scoring...")
        scores = defaultdict(int)
        for p in self.players:
            scores[p.name] += sum(p.tokens)
        camels_counts = [(p.name, len(p.camels)) for p in self.players]
        camels_counts.sort(key=lambda x: x[1], reverse=True)
        if camels_counts[0][1] > camels_counts[1][1]:
            scores[camels_counts[0][0]] += 5
            self.gui.show_message(f"{camels_counts[0][0]} gets camel bonus 5 points!")
        for p in self.players:
            self.gui.show_message(f"{p.name} final score: {scores[p.name]}")
        winner = max(scores, key=scores.get)
        self.gui.show_message(f"\nWinner is {winner}!")

    def play(self) -> None:
        while not self.is_game_over():
            self.play_turn()
        self.final_scoring()