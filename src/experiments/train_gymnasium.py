# train.py
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from src.core.players.gymnasium.environment import JaipurEnv

# Create environment
env = make_vec_env(lambda: JaipurEnv(), n_envs=4)

# Create model
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    learning_rate=0.0003,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.0
)

# Evaluation callback
eval_callback = EvalCallback(
    env,
    best_model_save_path="./logs/",
    log_path="./logs/",
    eval_freq=10000,
    deterministic=True,
    render=False
)

# Train the model
model.learn(total_timesteps=1_000_000, callback=eval_callback)

# Save the model
model.save("jaipur_ppo")