import json
from pathlib import Path


def load_settings():
    root = Path(__file__).resolve().parent.parent
    settings_file = root / "config" / "settings.json"

    with settings_file.open("r", encoding="utf-8") as file:
        settings = json.load(file)

    settings["_project_root"] = root

    for key in (
        "memory_file",
        "piper_executable",
        "piper_model",
        "piper_config",
    ):
        settings[key] = str(root / settings[key])

    return settings