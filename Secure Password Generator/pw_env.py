import gymnasium as gym
from gymnasium import spaces
import numpy as np
from zxcvbn import zxcvbn
import string

class PasswordGenEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, max_len=24, prefix_len=24):
        super().__init__()
        self.max_len = max_len
        self.prefix_len = prefix_len

        self.charset = list(
            string.ascii_lowercase +
            string.ascii_uppercase +
            string.digits +
            "!@#$%^&*()-_=+[]{};:,.<>/? "
        )

        self.end_token = "<END>"
        self.charset.append(self.end_token)

        self.V = len(self.charset)

        self.idx2ch = {i: ch for i, ch in enumerate(self.charset)}
        self.ch2idx = {ch: i for i, ch in self.idx2ch.items()}

        self.pad_idx = self.V  

        self.observation_space = spaces.Box(
            low=0,
            high=self.pad_idx,
            shape=(self.prefix_len,),
            dtype=np.int32
        )

        self.action_space = spaces.Discrete(self.V)

        self.seq = []

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.seq = []
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        ch = self.idx2ch[int(action)]
        terminated = False
        truncated = False
        reward = 0.0

        if ch == self.end_token:
            terminated = True
            reward = self._final_reward()
        elif len(self.seq) >= self.max_len:
            truncated = True
            reward = self._final_reward()
        else:
            self.seq.append(ch)
            reward = -0.01

        obs = self._get_obs()
        return obs, reward, terminated, truncated, {}

    def _get_obs(self):
        arr = [self.ch2idx[ch] for ch in self.seq]
        if len(arr) < self.prefix_len:
            arr += [self.pad_idx] * (self.prefix_len - len(arr))
        else:
            arr = arr[:self.prefix_len]
        return np.array(arr, dtype=np.int32)

    def _final_reward(self):
        pw = "".join(self.seq)
        if not pw:
            return -1.0

        zx = zxcvbn(pw)
        score = zx["score"]

        length_score = min(len(pw) / 20, 1)

        reward = score + length_score
        return float(np.tanh(reward))

    def render(self):
        print("Generated password:", "".join(self.seq))
