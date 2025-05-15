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
        # Ensure each nurse is assigned between 3 and 5 patients
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for patient in patients) >= 3
        )
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for patient in patients) <= 5
        )

        # Ensure the total complexity of assigned patients does not exceed the nurse's capacity
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] * patient['complexity'] for patient in patients)
            <= nurse['max_capacity']
        )

        # Ensure that if a nurse is assigned a patient with complexity 3,
        # they are only assigned other patients with complexity 3.
        complexity_3_patients = [
            assignments[(nurse['id'], patient['id'])] for patient in patients if patient['complexity'] == 3
        ]
        other_patients = [
            assignments[(nurse['id'], patient['id'])] for patient in patients if patient['complexity'] != 3
        ]

        # If a nurse is assigned any patient with complexity 3, force all other assignments to be 0.
        for complexity_3 in complexity_3_patients:
            for other in other_patients:
                model.Add(complexity_3 + other <= 1)

    # Ensure that each patient is assigned to exactly one nurse
    for patient in patients:
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for nurse in nurses) == 1
        )

    # Objective: Maximize continuity of care
    continuity = []
    for (nurse_id, patient_id), assigned in assignments.items():
        if history.get(str(patient_id)) == nurse_id:
            continuity.append(assigned)
    model.Maximize(sum(continuity))

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