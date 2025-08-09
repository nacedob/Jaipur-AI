from abc import ABC, abstractmethod
from typing import List


class BasePlayerView(ABC):
    name: str
    hand: dict
    camels: int
    tokens: int


class BaseMarketView(ABC):
    goods: dict
    camels: int


class BaseGUI(ABC):
    @abstractmethod
    def show_game_state(self, players: List[BasePlayerView], market: BaseMarketView) -> None:
        pass
    @abstractmethod
    def show_turn_options(self, players: List[BasePlayerView], market: BaseMarketView) -> None:
        pass
