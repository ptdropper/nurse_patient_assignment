import json

def get_static_version():
    try:
        with open("version.txt") as f:
            return f.read().strip()
    except Exception:
        return "unknown"

def save_schedule(schedule, filename='data/schedule.json'):
    with open(filename, 'w') as f:
        json.dump(schedule, f, indent=4)

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)