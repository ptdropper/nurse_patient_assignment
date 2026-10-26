from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os, json
from scheduler.solver import load_data
from scheduler.scheduler import assign_nurses_to_patients
from scheduler.utils import save_schedule, get_static_version

app = Flask(__name__, static_folder='../static', template_folder="../templates")


NURSES_JSON_PATH = "data/nurses.json"

def load_nurses():
    if os.path.exists(NURSES_JSON_PATH):
        with open(NURSES_JSON_PATH, "r") as f:
            nurses = json.load(f)
        if nurses:
            return nurses
    return [{"id": 1, "name": "Nurse 1", "max_capacity": 0}]

def save_nurses(nurses):
    with open(NURSES_JSON_PATH, "w") as f:
        json.dump(nurses, f, indent=2)


def normalize_nurses(nurses, count):
    existing = {int(n.get("id", idx + 1)): n for idx, n in enumerate(nurses)}
    normalized = []
    for i in range(1, count + 1):
        current = existing.get(i, {})
        normalized.append({
            "id": i,
            "name": current.get("name") or f"Nurse {i}",
            "max_capacity": int(current.get("max_capacity", 0) or 0),
        })
    return normalized

@app.route("/nurse_capacity", methods=["POST"])
def nurse_capacity():
    try:
        nurse_count = int(request.form.get("nurse_count", 6))
    except (TypeError, ValueError):
        nurse_count = 6
    nurse_count = max(1, min(20, nurse_count))

    nurses = normalize_nurses(load_nurses(), nurse_count)
    for i in range(1, nurse_count + 1):
        name = request.form.get(f"nurse_name_{i}", f"Nurse {i}")
        try:
            max_capacity = int(request.form.get(f"nurse_capacity_{i}", 0))
        except (ValueError, TypeError):
            max_capacity = 0
        nurses[i - 1]["name"] = name
        nurses[i - 1]["max_capacity"] = max_capacity
    save_nurses(nurses)
    # Redirect to the index page after saving
    return redirect(url_for("index"))

@app.route('/static/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('../static', path)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/favicon.ico')
def serve_favicon():
    try:
        return send_from_directory('../static', 'favicon.ico')
    except FileNotFoundError:
        return "", 204

@app.route("/", methods=["GET", "POST"])
def index():
    version = get_static_version()

    # Load data
    nurses, patients, history = load_data()
    nurse_count = len(nurses) if nurses else 6

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
            if room_distance_max is not None:
                patient['room_distance_max'] = int(room_distance_max)
        # Save updated patient data
        save_schedule(patients, filename="../data/patients.json")

        # Generate the schedule
        try:
            schedule = assign_nurses_to_patients(nurses, patients, history, max_row_diff=max_row_difference)
            return render_template("index.html", patients=patients, schedule=schedule, success=True,
                                   max_row_diff=max_row_difference, version=version, nurses=nurses,
                                   nurse_count=nurse_count)
        except Exception as e:
            # Log the error for debugging
            print(f"Error during scheduling: {e}")

    # Render the page with default data
    return render_template("index.html", patients=patients, schedule=[],
                           max_row_diff=max_row_difference, version=version, nurses=nurses,
                           nurse_count=nurse_count)


if __name__ == "__main__":
    # auto reload for convenience but breaks PyCharm debugger
    # app.run(debug=True)

    # Heroku deployment configuration and local testing
    port = int(os.environ.get('PORT', 5000))  # Use Heroku's PORT or default to 5000
    app.run(host='0.0.0.0', port=port)

    # provide for PyCharm debugging by telling Flask to not use reloader
    #app.run(debug=True, use_reloader=False)