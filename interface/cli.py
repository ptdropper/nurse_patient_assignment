from scheduler.solver import load_data
from scheduler.scheduler import assign_nurses_to_patients

def main():
    nurses, patients, history = load_data()
    schedule = assign_nurses_to_patients(nurses, patients, history)
    print("\nSchedule for Tomorrow:")
    for entry in schedule:
        print(f"Nurse {entry['nurse']} is assigned to patients {entry['patients']}")

if __name__ == "__main__":
    main()