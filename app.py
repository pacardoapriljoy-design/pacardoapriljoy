import sqlite3
import requests
from pathlib import Path
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = Path(__file__).resolve().parent / "students.db"


# CONNECT TO DATABASE
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# STUDENT INFORMATION
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2026-00001",
        "name": "April Joy Pacardo",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


# HELLO API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({"message": f"Hello, {name}!"})


# HOBBIES API
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


# STUDY HOURS API
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


# DISPLAY ALL STUDENTS - LAB 7
@app.route('/students')
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# DISPLAY ONE STUDENT - LAB 7
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# FILTER STUDENTS BY SECTION - LAB 7
@app.route('/students/section/<section>')
def get_students_by_section(section):
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students WHERE section = ?',
        (section,)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ===================================
# LABORATORY ACTIVITY 8 - CRUD API
# ===================================

# READ ALL STUDENTS - GET
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# CREATE STUDENT - POST
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True) or {}

    required_fields = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == '':
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        year = int(data['year'])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number."}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO students
        (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data['student_id'],
            data['name'],
            data['program'],
            year,
            data['section']
        )
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added successfully",
        "id": new_id
    }), 201


# READ ONE STUDENT - GET
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# UPDATE STUDENT - PUT
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True) or {}

    required_fields = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == '':
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        year = int(data['year'])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number."}), 400

    conn = get_db_connection()

    existing_student = conn.execute(
        'SELECT id FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    if existing_student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute(
        """
        UPDATE students
        SET student_id = ?,
            name = ?,
            program = ?,
            year = ?,
            section = ?
        WHERE id = ?
        """,
        (
            data['student_id'],
            data['name'],
            data['program'],
            year,
            data['section'],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student updated successfully"
    })


# DELETE STUDENT - DELETE
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    existing_student = conn.execute(
        'SELECT id FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    if existing_student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute(
        'DELETE FROM students WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student deleted successfully"
    })


# ===================================
# CLASSMATE API - COURSES
# ===================================

@app.route('/api/classmate-courses', methods=['GET'])
def get_classmate_courses():

    classmate_url = "https://palencia-shamainejoyce.onrender.com/courses"

    try:
        response = requests.get(
            classmate_url,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Classmate API request timed out. Please try again."
        }), 504

    except requests.exceptions.HTTPError:
        return jsonify({
            "error": "Classmate API returned an HTTP error.",
            "status_code": response.status_code
        }), 502

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Cannot connect to classmate's API."
        }), 502

    except ValueError:
        return jsonify({
            "error": "Invalid JSON response from classmate API."
        }), 502

    except requests.exceptions.RequestException as error:
        return jsonify({
            "error": str(error)
        }), 502


# RUN FLASK APPLICATION
if __name__ == '__main__':
    app.run(debug=True)
