import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

DEFAULT_SETTINGS = {
    "snake_color": [0, 180, 0],
    "grid": True,
    "sound": True
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except json.JSONDecodeError:
        settings = DEFAULT_SETTINGS.copy()

    # если в json не хватает ключей — добавляем
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value

    save_settings(settings)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)