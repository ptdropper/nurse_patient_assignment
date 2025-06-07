from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
from scheduler.solver import load_data
from scheduler.scheduler import assign_nurses_to_patients
from scheduler.utils import save_schedule

app = Flask(__name__, static_folder='../static', template_folder="../templates")

# Serve static HTML/CSS
@app.route('/')
def serve_index():
    return send_from_directory('../templates', 'index.html')

# Serve other static files
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('../static', path)
    except FileNotFoundError:
        return "File not found", 404

@app.route("/", methods=["GET", "POST"])
def index():
    # Load data
    nurses, patients, history = load_data()
    # Get max_row_diff from form, default to 1 if not set
    if request.method == 'POST':
        try:
            max_row_difference = int(request.form.get('max_row_diff', 1))
        except ValueError:
            max_row_difference = 20
    else:
        max_row_difference = 99

    if request.method == "POST":
        # Update patient complexities from the form
        for patient in patients:
            complexity = request.form.get(f"complexity_{patient['id']}")
            if complexity:
                patient['complexity'] = int(complexity)
        room_distance_max = request.form.get(f"room_distance_max_{patient['id']}")
        # Save updated patient data
        save_schedule(patients, filename="data/patients.json")

        # Generate the schedule
        try:
            schedule = assign_nurses_to_patients(nurses, patients, history, max_row_diff=max_row_difference)
            return render_template("index.html", patients=patients, schedule=schedule, success=True, max_row_diff=max_row_difference)
        except Exception as e:
            return render_template("index.html", patients=patients, schedule=[], error=str(e), max_row_diff=max_row_difference)
    
    # Render the page with default data
    return render_template("index.html", patients=patients, schedule=[], max_row_diff=max_row_difference)

if __name__ == "__main__":
    # auto reload for convenience but breaks PyCharm debugger
    # app.run(debug=True)

    port = int(os.environ.get('PORT', 5000))  # Use Heroku's PORT or default to 5000
    app.run(host='0.0.0.0', port=port)

    # provide for PyCharm debugging by telling Flask to not use reloader
    #app.run(debug=True, use_reloader=False)