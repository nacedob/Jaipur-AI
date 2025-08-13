# trained_ai_player.py
from typing import List, Dict
import numpy as np
from stable_baselines3 import PPO
from ...market import Market
from ...deck import Deck, Card
from ..base_player import BasePlayer
from .environment import JaipurEnv

class TrainedAIPlayer(BasePlayer):
    def __init__(self, name: str = "Trained AI", model_path: str = None):
        super().__init__(name)
        self.env = JaipurEnv()
        if model_path:
            self.model = PPO.load(model_path)
        else:
            self.model = None

    def take_turn(self, market: Market, deck: Deck) -> bool:
        if not self.model:
            return False  # Fallback to random if no model loaded
            
        # Get current observation
        obs = self._get_observation(market)
        
        # Get action from model
        action, _ = self.model.predict(obs, deterministic=True)
        
        # Execute action
        if action < 7:  # Take single good
            card = list(Card)[action]
            return self.take_single_good(card, market, deck)
        elif action == 7:  # Take all camels
            return self.take_camels(market, deck)
        elif action < 14:  # Sell goods
            card = list(Card)[action - 8]
            count = self.hand.count(card)
            if count > 0:
                return self.sell_goods(card, count)
        return False

    def _get_observation(self, market: Market) -> Dict[str, np.ndarray]:
        """Convert current game state to observation for the model"""
        card_order = list(Card)
        market_counts = [market.cards.count(c) for c in card_order]
        hand_counts = [self.hand.count(c) for c in card_order]
        
        return {
            'market': np.array(market_counts, dtype=np.int32),
            'hand': np.array(hand_counts, dtype=np.int32),
            'camels': np.array([len(self.camels)], dtype=np.int32),
            'tokens': np.array([sum(self.tokens)], dtype=np.int32),
            'opponent_camels': np.array([0], dtype=np.int32),  # Placeholder
            'opponent_tokens': np.array([0], dtype=np.int32),  # Placeholder
            'transactions': np.array([0]*7, dtype=np.int32)    # Placeholder
        }