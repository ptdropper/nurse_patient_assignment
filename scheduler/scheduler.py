from ortools.sat.python import cp_model

def assign_nurses_to_patients(nurses, patients, history):
    model = cp_model.CpModel()

    # Variables
    assignments = {}
    for nurse in nurses:
        for patient in patients:
            assignments[(nurse['id'], patient['id'])] = model.NewBoolVar(f'nurse_{nurse["id"]}_patient_{patient["id"]}')

    # Constraints
    for nurse in nurses:
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] * patient['complexity'] for patient in patients)
            <= nurse['max_capacity']
        )

    for patient in patients:
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for nurse in nurses) == 1
        )

    continuity = []
    for (nurse_id, patient_id), assigned in assignments.items():
        if history.get(str(patient_id)) == nurse_id:
            continuity.append(assigned)
    model.Maximize(sum(continuity))

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