import json
from pathlib import Path

from scheduler.paths import SCHEDULE_FILE, VERSION_FILE, resolve_project_path


def get_static_version():
    try:
        with VERSION_FILE.open(encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "unknown"


def save_schedule(schedule, filename: str | Path = SCHEDULE_FILE):
    path = resolve_project_path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=4)


def load_json_file(filepath: str | Path):
    path = resolve_project_path(filepath)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
