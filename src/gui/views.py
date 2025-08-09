from dataclasses import dataclass

@dataclass
class PlayerView:
    name: str
    hand: dict
    camels: int
    tokens: int


@dataclass
class MarketView:
    goods: dict
    camels: int