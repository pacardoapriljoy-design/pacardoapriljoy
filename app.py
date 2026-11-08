
import sqlite3
import requests
<<<<<<< HEAD

=======
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
from pathlib import Path
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DATABASE LOCATION
DATABASE = Path(__file__).resolve().parent / "students.db"

<<<<<<< HEAD
# CLASSMATE API
CLASSMATE_API_URL = "https://francineescultura-4.onrender.com/courses"


# ===================================
# DATABASE CONNECTION
# ===================================

=======

# CONNECT TO DATABASE
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
def get_db_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# ===================================
# INITIALIZE DATABASE
# ===================================

def init_db():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL

        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    if count == 0:

        conn.execute("""
            INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "2026-00001",
            "April Joy Pacardo",
            "BSIT",
            3,
            "Dijkstra"
        ))

    conn.commit()
    conn.close()

    print("Database initialized successfully!")


# ===================================
# HOME PAGE
# ===================================

@app.route('/')
def home():

    return render_template('index.html')


# ===================================
# STUDENT INFORMATION API
# ===================================

@app.route('/student')
def get_student():

    return jsonify({
        "student_id": "2026-00001",
        "name": "April Joy Pacardo",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


# ===================================
# HELLO API
# ===================================

@app.route('/hello')
def say_hello():

    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# ===================================
# HOBBIES API
# ===================================

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


# ===================================
# STUDY HOURS API
# ===================================

@app.route('/studyhours')
def study_hours():

    hours = request.args.get('hours')

    if hours is None:
<<<<<<< HEAD

=======
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
        return jsonify({
            "error": "Please provide your study hours."
        }), 400

    try:

        hours = float(hours)
<<<<<<< HEAD

    except (ValueError, TypeError):

=======
    except ValueError:
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
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


<<<<<<< HEAD
# ===================================
# LAB 7 - DISPLAY ALL STUDENTS
# ===================================

=======
# DISPLAY ALL STUDENTS - LAB 7
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
@app.route('/students')
def get_students():

    conn = get_db_connection()

    try:

        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

        return jsonify([
            dict(student) for student in students
        ])

    finally:

        conn.close()


<<<<<<< HEAD
# ===================================
# LAB 7 - DISPLAY ONE STUDENT
# ===================================

=======
# DISPLAY ONE STUDENT - LAB 7
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
@app.route('/students/<int:id>')
def get_student_by_id(id):

    conn = get_db_connection()

    try:

        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if student is None:

            return jsonify({
                "error": "Student not found."
            }), 404

        return jsonify(dict(student))

    finally:

        conn.close()


<<<<<<< HEAD
# ===================================
# LAB 7 - FILTER BY SECTION
# ===================================

=======
# FILTER STUDENTS BY SECTION - LAB 7
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
@app.route('/students/section/<section>')
def get_students_by_section(section):

    conn = get_db_connection()

    try:

        students = conn.execute(
            "SELECT * FROM students WHERE section = ?",
            (section,)
        ).fetchall()

        return jsonify([
            dict(student) for student in students
        ])

    finally:

        conn.close()


# ===================================
# LAB 8 - READ ALL STUDENTS
# GET
# ===================================

@app.route('/api/students', methods=['GET'])
def api_students():

    conn = get_db_connection()

    try:

        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

        return jsonify([
            dict(student) for student in students
        ])

    finally:

        conn.close()


# ===================================
# VALIDATE STUDENT DATA
# ===================================

def validate_student(data):

    if not isinstance(data, dict):

        return None, "Invalid student information."

    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    for field in required_fields:

        if field not in data or data[field] is None:

            return None, f"Missing required field: {field}"

        if not str(data[field]).strip():

            return None, f"{field} is required."

    try:

        year = int(data["year"])

    except (ValueError, TypeError):

        return None, "Year must be a number."

    if year < 1 or year > 5:

        return None, "Year must be between 1 and 5."

    student = {

        "student_id": str(data["student_id"]).strip(),
        "name": str(data["name"]).strip(),
        "program": str(data["program"]).strip(),
        "year": year,
        "section": str(data["section"]).strip()

    }

    return student, None


# ===================================
# LAB 8 - CREATE STUDENT
# POST
# ===================================

@app.route('/api/students', methods=['POST'])
def add_student():

    data = request.get_json(silent=True)

    student, error = validate_student(data)

    if error:

        return jsonify({
            "error": error
        }), 400

    conn = get_db_connection()

    try:

        cursor = conn.execute("""
            INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student["student_id"],
            student["name"],
            student["program"],
            student["year"],
            student["section"]
        ))

        conn.commit()

        return jsonify({

            "message": "Student added successfully!",
            "id": cursor.lastrowid

        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "Unable to add student."
        }), 409

    finally:

        conn.close()


# ===================================
# LAB 8 - READ ONE STUDENT
# GET
# ===================================

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):

    conn = get_db_connection()

    try:

        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if student is None:

            return jsonify({
                "error": "Student not found."
            }), 404

        return jsonify(dict(student))

    finally:

        conn.close()


# ===================================
# LAB 8 - UPDATE STUDENT
# PUT
# ===================================

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):

    data = request.get_json(silent=True)

    student, error = validate_student(data)

    if error:

        return jsonify({
            "error": error
        }), 400

    conn = get_db_connection()

    try:

        existing = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if existing is None:

            return jsonify({
                "error": "Student not found."
            }), 404

        conn.execute("""
            UPDATE students

            SET student_id = ?,
                name = ?,
                program = ?,
                year = ?,
                section = ?

            WHERE id = ?
        """, (
            student["student_id"],
            student["name"],
            student["program"],
            student["year"],
            student["section"],
            id
        ))

        conn.commit()

        return jsonify({
            "message": "Student updated successfully!"
        })

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "Unable to update student."
        }), 409

    finally:

        conn.close()


# ===================================
# LAB 8 - DELETE STUDENT
# DELETE
# ===================================

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):

    conn = get_db_connection()

    try:

        existing = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if existing is None:

            return jsonify({
                "error": "Student not found."
            }), 404

        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

        conn.commit()

        return jsonify({
            "message": "Student deleted successfully!"
        })

    finally:

        conn.close()


# ===================================
<<<<<<< HEAD
# LAB 8 - CLASSMATE API
# FRANCINE ESCULTURA
# COURSES - READ ONLY
=======
# CLASSMATE API - COURSES
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
# ===================================

@app.route('/api/classmate-courses', methods=['GET'])
def get_classmate_courses():

<<<<<<< HEAD
    try:

        response = requests.get(
            CLASSMATE_API_URL,
            headers={
                "Accept": "application/json"
            },
=======
    classmate_url = "https://palencia-shamainejoyce.onrender.com/courses"

    try:
        response = requests.get(
            classmate_url,
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

<<<<<<< HEAD
        # HANDLE COURSE JSON FORMATS

        if isinstance(data, list):

            courses = data

        elif isinstance(data, dict) and isinstance(data.get("courses"), list):

            courses = data["courses"]

        elif isinstance(data, dict) and isinstance(data.get("data"), list):

            courses = data["data"]

        else:

            return jsonify({
                "error": "Invalid course API response."
            }), 502

        # RETURN COURSE RECORDS ONLY

        return jsonify(courses)

    except requests.exceptions.Timeout:

        return jsonify({
            "error": "Classmate API request timed out."
        }), 504

    except requests.exceptions.HTTPError:

=======
        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Classmate API request timed out. Please try again."
        }), 504

    except requests.exceptions.HTTPError:
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
        return jsonify({
            "error": "Classmate API returned an HTTP error.",
            "status_code": response.status_code
        }), 502

    except requests.exceptions.ConnectionError:
<<<<<<< HEAD

        return jsonify({
            "error": "Cannot connect to Francine's API."
        }), 502

    except ValueError:

=======
        return jsonify({
            "error": "Cannot connect to classmate's API."
        }), 502

    except ValueError:
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
        return jsonify({
            "error": "Invalid JSON response from classmate API."
        }), 502

<<<<<<< HEAD
    except requests.exceptions.RequestException:

        return jsonify({
            "error": "Unable to retrieve classmate records."
        }), 502


# ===================================
=======
    except requests.exceptions.RequestException as error:
        return jsonify({
            "error": str(error)
        }), 502


>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
# RUN FLASK APPLICATION
# ===================================

if __name__ == '__main__':

    init_db()

    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )
