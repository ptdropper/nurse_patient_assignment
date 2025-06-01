from ortools.sat.python import cp_model

def assign_nurses_to_patients(nurses, patients, history, max_row_diff):
    model = cp_model.CpModel()

    # Variables
    assignments = {}
    for nurse in nurses:
        for patient in patients:
            assignments[(nurse['id'], patient['id'])] = model.NewBoolVar(f'nurse_{nurse["id"]}_patient_{patient["id"]}')

    # Constraints
    for nurse in nurses:
        # Ensure each nurse is assigned between 3 and 6 patients
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for patient in patients) >= 3
        )
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] for patient in patients) <= 6
        )

        # Ensure the total complexity of assigned patients does not exceed the nurse's capacity
        model.Add(
            sum(assignments[(nurse['id'], patient['id'])] * patient['complexity'] for patient in patients)
            <= nurse['max_capacity']
        )

        # Complexity-3 logic (same as previous)
        # If a nurse has a patient with complexity 3, they should be assigned only complexity 3
        complexity_3_patients = [
            assignments[(nurse['id'], patient['id'])] for patient in patients if patient['complexity'] == 3
        ]
        other_patients = [
            assignments[(nurse['id'], patient['id'])] for patient in patients if patient['complexity'] != 3
        ]
        for complexity_3 in complexity_3_patients:
            for other in other_patients:
                model.Add(complexity_3 + other <= 1)

        # --- Row constraint ---
        # Rooms are arranged in as rows down the hall, so we need to ensure that nurses do not
        # have patients assigned to distant rows.
        # Use max_row_diff to limit the distance between the rows of assigned patients.
        # Example

        # Row   ID numbers. (rooms are on each side of a hallway, left and right)
        #  1    1 and 30
        #  2    2 and 29
        #  3    3 and 28
        # ...
        # For each nurse, collect row numbers of assigned patients
        #  Example patient data structure
        #  patients{
        #    "id": 2,
        #    "bed": "102",
        #    "row": 2,
        #    "complexity": 3
        # }
        #
        row_numbers = list(set(patient['row'] for patient in patients))
        row_used = {}
        for row in row_numbers:
            row_used[row] = model.NewBoolVar(f"nurse_{nurse['id']}_row_{row}_used")
            # If nurse is assigned any patient in this row, row_used[row] = 1
            model.AddMinEquality(
                row_used[row],
                [assignments[(nurse['id'], patient['id'])] for patient in patients if patient['row'] == row]
                if any(patient['row'] == row for patient in patients)
                else [model.NewConstant(0)]
            )

        # The row numbers used by this nurse assigned patients
        row_expr = [row * row_used[row] for row in row_numbers]
        # Compute min and max row values they are assigned to
        min_row = model.NewIntVar(1, max(row_numbers), f"nurse_{nurse['id']}_minrow")
        max_row = model.NewIntVar(1, max(row_numbers), f"nurse_{nurse['id']}_maxrow")
        # Set min_row and max_row
        model.AddMinEquality(min_row, [row for row in row_numbers for _ in (0,)] +
                                      [row + (1 - row_used[row]) * (max(row_numbers)) for row in row_numbers])
        model.AddMaxEquality(max_row, [row_used[row] * row for row in row_numbers])

        # Require that max_row - min_row <= distance_max if the nurse has any assigned patients
        # Find a way to force clustering
        model.Add(max_row - min_row < max_row_diff).OnlyEnforceIf(row_used[row] for row in row_numbers)

    # Each patient assigned to exactly one nurse
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