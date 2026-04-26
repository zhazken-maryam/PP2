import json
import os


SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 180, 0],
    "grid": True,
    "sound": True
}


def load_settings():
    """Loads settings from JSON file."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Saves settings to JSON file."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)
