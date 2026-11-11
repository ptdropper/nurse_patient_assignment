import json
from scheduler import scheduler
from scheduler.paths import HISTORY_FILE, NURSES_FILE, PATIENTS_FILE


def load_data():
    with NURSES_FILE.open(encoding="utf-8") as f:
        nurses_data = json.load(f)
    with PATIENTS_FILE.open(encoding="utf-8") as f:
        patients_data = json.load(f)
    with HISTORY_FILE.open(encoding="utf-8") as f:
        history_data = json.load(f)
    return nurses_data, patients_data, history_data


if __name__ == "__main__":
    nurses, patients, history = load_data()
    schedule = scheduler.assign_nurses_to_patients(nurses, patients, history, max_row_diff=2)
    print("Schedule for Tomorrow:")
    for entry in schedule:
        print(f"{entry['nurse']} -> Patients: {entry['patients']}")
