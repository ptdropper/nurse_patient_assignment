from ortools.sat.python import cp_model

def assign_nurses_to_patients(nurses, patients, history, max_row_diff):
    model = cp_model.CpModel()
    assignments = {}
    for nurse in nurses:
        for patient in patients:
            assignments[(nurse['id'], patient['id'])] = model.NewBoolVar(f'nurse_{nurse["id"]}_patient_{patient["id"]}')

    row_numbers = sorted(set(patient['row'] for patient in patients))
    min_row, max_row = min(row_numbers), max(row_numbers)
    half_max_row = max_row_diff // 2

    for nurse in nurses:
        center_row = model.NewIntVar(min_row, max_row, f"nurse_{nurse['id']}_center_row")

        # Each nurse must be assigned between 3 and 6 patients
        model.Add(sum(assignments[(nurse['id'], patient['id'])] for patient in patients) >= 3)
        model.Add(sum(assignments[(nurse['id'], patient['id'])] for patient in patients) <= 6)

        # Total complexity constraint
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] * patient['complexity'] for patient in patients)
            <= nurse['max_capacity']
        )

        # --- Row clustering constraint ---
        for patient in patients:
            # diff = |patient_row - center_row|
            diff = model.NewIntVar(0, max_row - min_row, f'diff_{nurse["id"]}_{patient["id"]}')
            model.AddAbsEquality(diff, patient['row'] - center_row)
            model.Add(diff <= half_max_row).OnlyEnforceIf(assignments[(nurse['id'], patient['id'])])
            # Only allow assignment if within range
            model.Add(diff <= half_max_row).OnlyEnforceIf(assignments[(nurse['id'], patient['id'])])

    # Each patient assigned to exactly one nurse
    for patient in patients:
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for nurse in nurses) == 1
        )

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        schedule = []
        for nurse in nurses:
            assigned_patients = [
                patient['id']
                for patient in patients
                if solver.Value(assignments[(nurse['id'], patient['id'])])
            ]
            schedule.append({"nurse": nurse['name'], "patients": assigned_patients})
        return schedule
    else:
        raise Exception("No optimal solution found.")