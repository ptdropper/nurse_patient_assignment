# Nurse Patient Assignment 

## Overview
A Python-based solution to suggest nurse-patient assignments for the next shift based on:
- Nurse availability and capacity.
- Patient bed assignments.
- Patient complexity of care.
- Previous assignment consistency.
- Room availability.
- Distance between nurses and patient rooms.

## Features
- Assigns nurses to patients and rooms while respecting complexity and capacity constraints.
- Prioritizes continuity of care. 
- Generates optimal schedules using Google OR-Tools.

## Project Structure
```plaintext
nurse_scheduler/
├── data/               # Input data for nurses, patients, and history
├── scheduler/          # Core scheduling logic
├── interface/          # CLI and optional web interface
├── tests/              # Unit tests
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   export PYTHONPATH=$(pwd):$PYTHONPATH
   ```

2. Run the Web CLI:
   ```bash
   export PYTHONPATH=$(pwd):$PYTHONPATH
   python interface/web.py
   ```

3. View the generated schedule in the console.

## Dependencies
- Python 3.12
- OR-Tools

