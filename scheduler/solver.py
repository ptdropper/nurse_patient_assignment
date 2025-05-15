import json
from scheduler import scheduler

def load_data():
    with open('data/nurses.json') as f:
        nurses = json.load(f)
    with open('data/patients.json') as f:
        patients = json.load(f)
    with open('data/history.json') as f:
        history = json.load(f)
    return nurses, patients, history

if __name__ == "__main__":
    nurses, patients, history = load_data()
    schedule = scheduler.assign_nurses_to_patients(nurses, patients, history)
    print("Schedule for Tomorrow:")
    for entry in schedule:
        print(f"{entry['nurse']} -> Patients: {entry['patients']}")