"""Centralized, working-directory-independent application paths."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(path: str | Path) -> Path:
    """Resolve a path relative to the project root unless it is already absolute."""
    resolved = Path(path).expanduser()
    if not resolved.is_absolute():
        resolved = PROJECT_ROOT / resolved
    return resolved.resolve()


# Deployments can keep mutable data outside the source checkout by setting this.
# Relative values are interpreted relative to PROJECT_ROOT.
DATA_DIR = resolve_project_path(os.environ.get("NURSE_PATIENT_DATA_DIR", "data"))
NURSES_FILE = DATA_DIR / "nurses.json"
PATIENTS_FILE = DATA_DIR / "patients.json"
HISTORY_FILE = DATA_DIR / "history.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"

STATIC_DIR = PROJECT_ROOT / "static"
TEMPLATE_DIR = PROJECT_ROOT / "templates"
VERSION_FILE = PROJECT_ROOT / "version.txt"
