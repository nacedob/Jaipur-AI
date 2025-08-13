from abc import ABC, abstractmethod
from typing import List
from .views import PlayerView, MarketView

class BaseGUI(ABC):
    @abstractmethod
    def show_game_state(self, players: List[PlayerView], market: MarketView) -> None:
        pass
    @abstractmethod
    def show_turn_options(self, players: List[PlayerView], market: MarketView) -> None:
        pass
