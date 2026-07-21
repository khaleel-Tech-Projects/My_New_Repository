from stable_baselines3 import PPO
from pw_env import PasswordGenEnv
from zxcvbn import zxcvbn

def sample_passwords(model_path, n=20):
    env = PasswordGenEnv()
    model = PPO.load(model_path)

    results = []
    for _ in range(n):
        obs, info = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=False)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        pw = "".join(env.seq)

        if not pw.strip():
            continue

        zx = zxcvbn(pw)
        results.append((pw, zx))

    return results

if __name__ == "__main__":
    out = sample_passwords("pw_ppo", n=10)
    for pw, zx in out:
        print(f"{pw} | score: {zx['score']} | guesses: {zx['guesses']}")
