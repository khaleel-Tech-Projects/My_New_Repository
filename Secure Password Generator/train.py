from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from pw_env import PasswordGenEnv

def main():
    env = make_vec_env(PasswordGenEnv, n_envs=1)

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        ent_coef=0.01
    )

    model.learn(total_timesteps=200000)
    model.save("pw_ppo")
    print("Model saved as pw_ppo.zip")

if __name__ == "__main__":
    main()
