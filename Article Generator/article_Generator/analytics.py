import json

LOG_FILE = "analytics.json"

def track_interaction(model, prompt, response):
    """Log user interactions."""
    log_entry = {
        "model": model,
        "prompt": prompt,
        "response": response,
    }
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f)

def get_analytics():
    """Retrieve analytics data."""
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        return []
