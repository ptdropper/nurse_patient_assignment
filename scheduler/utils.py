import json
import subprocess

def get_git_version():
    try:
        # Use 'git describe' to get the latest tag or commit
        version = subprocess.check_output(
            ['git', 'describe', '--tags', '--always'], stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return version
    except Exception:
        return "unknown"

def save_schedule(schedule, filename='data/schedule.json'):
    with open(filename, 'w') as f:
        json.dump(schedule, f, indent=4)

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)