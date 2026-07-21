from flask import Flask, render_template, request
from stable_baselines3 import PPO
from pw_env import PasswordGenEnv
from zxcvbn import zxcvbn
import numpy as np

app = Flask(__name__)

model = PPO.load("pw_ppo")
env = PasswordGenEnv()


def generate_password():
    obs, info = env.reset()
    done = False

    while not done:
        action, _ = model.predict(obs, deterministic=False)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

    pw = "".join(env.seq)
    if not pw.strip():
        return None

    zx = zxcvbn(pw)
    return {
        "password": pw,
        "score": zx["score"],
        "guesses": zx["guesses"]
    }


@app.route("/", methods=["GET", "POST"])
def index():
    passwords = []
    strength = {"Weak": 0, "Medium": 0, "Strong": 0}
    lengths = []
    guesses_log = []

    if request.method == "POST":
        count = int(request.form.get("count", 5))

        for _ in range(count):
            result = generate_password()
            if result:
                passwords.append(result)
                lengths.append(len(result["password"]))
                guesses_log.append(float(round(np.log10(float(result["guesses"]) + 1), 2)))


                if result["score"] >= 3:
                    strength["Strong"] += 1
                elif result["score"] == 2:
                    strength["Medium"] += 1
                else:
                    strength["Weak"] += 1

    return render_template(
        "index.html",
        passwords=passwords,
        strength=strength,
        lengths=lengths,
        guesses_log=guesses_log
    )


if __name__ == "__main__":
    app.run(debug=True)
