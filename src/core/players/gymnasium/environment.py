# jaipur_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Tuple, Optional
from ...game import Game
from ...deck import Card

class JaipurEnv(gym.Env):
    metadata = {'render_modes': ['human', 'ansi'], 'render_fps': 4}

    def __init__(self, render_mode: str = None):
        super().__init__()
        self.game = Game(player_types=['ai', 'ai'])  # Both players are AI for training
        self.current_player = self.game.players[0]
        self.opponent = self.game.players[1]
        self.render_mode = render_mode

        # Define action space
        # Actions: 
        # 0-6: Take single good (Diamond, Gold, Silver, Cloth, Spice, Leather, Camel)
        # 7: Take all camels
        # 8-13: Sell goods (Diamond, Gold, Silver, Cloth, Spice, Leather)
        # 14: Exchange (not implemented yet)
        self.action_space = spaces.Discrete(15)

        # Define observation space
        # Observation includes:
        # - Market goods counts (7 cards)
        # - Player hand counts (7 cards)
        # - Player camel count
        # - Player tokens
        # - Opponent visible info (camel count, tokens)
        # - Transaction counts (7 cards)
        self.observation_space = spaces.Dict({
            'market': spaces.Box(low=0, high=20, shape=(7,), dtype=np.int32),
            'hand': spaces.Box(low=0, high=10, shape=(7,), dtype=np.int32),
            'camels': spaces.Box(low=0, high=20, shape=(1,), dtype=np.int32),
            'tokens': spaces.Box(low=0, high=100, shape=(1,), dtype=np.int32),
            'opponent_camels': spaces.Box(low=0, high=20, shape=(1,), dtype=np.int32),
            'opponent_tokens': spaces.Box(low=0, high=100, shape=(1,), dtype=np.int32),
            'transactions': spaces.Box(low=0, high=5, shape=(7,), dtype=np.int32)
        })

    def _get_obs(self) -> Dict[str, np.ndarray]:
        """Convert game state to observation vector"""
        card_order = list(Card)
        market_counts = [self.game.market.cards.count(c) for c in card_order]
        hand_counts = [self.current_player.hand.count(c) for c in card_order]
        
        return {
            'market': np.array(market_counts, dtype=np.int32),
            'hand': np.array(hand_counts, dtype=np.int32),
            'camels': np.array([len(self.current_player.camels)], dtype=np.int32),
            'tokens': np.array([sum(self.current_player.tokens)], dtype=np.int32),
            'opponent_camels': np.array([len(self.opponent.camels)], dtype=np.int32),
            'opponent_tokens': np.array([sum(self.opponent.tokens)], dtype=np.int32),
            'transactions': np.array([self.game.transactions[c] for c in card_order], dtype=np.int32)
        }

    def reset(self, seed=None, options=None) -> Tuple[Dict, Dict]:
        super().reset(seed=seed)
        self.game = Game(player_types=['ai', 'ai'])
        self.current_player = self.game.players[0]
        self.opponent = self.game.players[1]
        observation = self._get_obs()
        info = {}
        
        if self.render_mode == 'human':
            self.render()
            
        return observation, info

    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        # Define action space
        # Actions: 
        # 0-6: Take single good (Diamond, Gold, Silver, Cloth, Spice, Leather, Camel)
        # 7: Take all camels
        # 8-13: Sell goods (Diamond, Gold, Silver, Cloth, Spice, Leather)
        # 14: Exchange (not implemented yet)
        
        terminated = False
        truncated = False
        reward = 0
        info = {}
        
        try:
            # Execute action
            if action < 7:  # Take single good
                card = list(Card)[action]
                if self.current_player.take_single_good(card, self.game.market, self.game.deck):
                    reward = 0.1  # Small reward for successful action
            elif action == 7:  # Take all camels
                if self.current_player.take_camels(self.game.market, self.game.deck):
                    reward = 0.2
            elif action < 14:  # Sell goods
                card = list(Card)[action - 8]
                count = self.current_player.hand.count(card)
                if count > 0:
                    if self.current_player.sell_goods(card, count):
                        reward = count * 0.5  # Reward based on number of cards sold
            
            # Switch players
            self.current_player, self.opponent = self.opponent, self.current_player
            
            # Check if game is over
            if self.game.is_game_over():
                terminated = True
                # Calculate final reward based on score difference
                my_score = sum(self.current_player.tokens) + (5 if len(self.current_player.camels) > len(self.opponent.camels) else 0)
                opp_score = sum(self.opponent.tokens) + (5 if len(self.opponent.camels) > len(self.current_player.camels) else 0)
                reward = my_score - opp_score
            
            observation = self._get_obs()
            
        except Exception as e:
            reward = -1  # Penalize invalid actions
            info['error'] = str(e)
        
        if self.render_mode == 'human':
            self.render()
            
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == 'human':
            print(f"\nCurrent Player: {self.current_player.name}")
            print(f"Market: {[c.name for c in self.game.market.cards]}")
            print(f"Hand: {[c.name for c in self.current_player.hand]}")
            print(f"Camels: {len(self.current_player.camels)}")
            print(f"Tokens: {sum(self.current_player.tokens)}")
        elif self.render_mode == 'ansi':
            return str(self.game)

    def close(self):
        pass