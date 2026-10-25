import json
from scheduler import scheduler
from os.path import join, dirname

DATA_DIR: str = dirname(__file__)

def load_data():
    with open(join(DATA_DIR, '../data/nurses.json')) as f:
        nurses_data = json.load(f)
    with open('../data/patients.json') as f:
        patients_data = json.load(f)
    with open('../data/history.json') as f:
        history_data = json.load(f)
    return nurses_data, patients_data, history_data

if __name__ == "__main__":
    nurses, patients, history = load_data()
    schedule = scheduler.assign_nurses_to_patients(nurses, patients, history, max_row_diff=2)
    print("Schedule for Tomorrow:")
    for entry in schedule:
        print(f"{entry['nurse']} -> Patients: {entry['patients']}")