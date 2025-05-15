from flask import Flask, render_template, request, redirect, url_for, jsonify
from scheduler.solver import load_data
from scheduler.scheduler import assign_nurses_to_patients
from scheduler.utils import save_schedule

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def index():
    # Load data
    nurses, patients, history = load_data()

    if request.method == "POST":
        # Update patient complexities from the form
        for patient in patients:
            complexity = request.form.get(f"complexity_{patient['id']}")
            if complexity:
                patient['complexity'] = int(complexity)

        # Save updated patient data
        save_schedule(patients, filename="data/patients.json")

        # Generate the schedule
        try:
            schedule = assign_nurses_to_patients(nurses, patients, history)
            return render_template("index.html", patients=patients, schedule=schedule, success=True)
        except Exception as e:
            return render_template("index.html", patients=patients, schedule=[], error=str(e))
    
    # Render the page with default data
    return render_template("index.html", patients=patients, schedule=[])

if __name__ == "__main__":
    app.run(debug=True)