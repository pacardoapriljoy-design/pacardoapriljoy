
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# DATABASE LOCATION
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / 'students.db'


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# 1. STUDENT INFORMATION API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2026-00001",
        "name": "April Joy Pacardo",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


# 2. GREETING API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# 3. HOBBIES API
@app.route('/hobbies')
def get_hobbies():
    return jsonify({
        "student": "April Joy Pacardo",
        "hobbies": [
            "Listening to music",
            "Reading books",
            "Watching movies",
            "Taking pictures",
            "Playing online games"
        ],
        "total_hobbies": 5
    })


# 4. STUDY HOURS API
@app.route('/studyhours')
def study_hours():
    hours = request.args.get('hours')

    if hours is None:
        return jsonify({
            "error": "Please provide your study hours."
        }), 400

    try:
        hours = float(hours)

    except ValueError:
        return jsonify({
            "error": "Invalid input. Please enter a number."
        }), 400

    if hours < 0 or hours > 24:
        return jsonify({
            "error": "Study hours must be between 0 and 24."
        }), 400

    if hours < 2:
        feedback = "You should spend more time studying."

    elif hours <= 5:
        feedback = "Keep up your good study habits!"

    else:
        feedback = "Great dedication! Remember to take breaks."

    return jsonify({
        "student": "April Joy Pacardo",
        "study_hours": hours,
        "feedback": feedback
    })


# 5. GET ALL STUDENTS FROM SQLITE DATABASE
@app.route('/students')
def get_students():

    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([
        dict(student) for student in students
    ])


# 6. GET ONE STUDENT BY ID
@app.route('/students/<int:id>')
def get_student_by_id(id):

    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# 7. ADDITIONAL TASK: FILTER STUDENTS BY SECTION
@app.route('/students/section/<section>')
def get_students_by_section(section):

    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students WHERE section = ?',
        (section,)
    ).fetchall()

    conn.close()

    return jsonify([
        dict(student) for student in students
    ])


# RUN FLASK APPLICATION
if __name__ == '__main__':
    app.run(debug=True)
