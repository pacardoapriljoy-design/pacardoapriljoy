
import os
import sqlite3
import requests

from flask import Flask, render_template, request, jsonify

# ===================================
# FLASK CONFIGURATION
# ===================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")

# Classmate's deployed API
CLASSMATE_BASE_URL = "https://francineescultura-4.onrender.com"
CLASSMATE_ENDPOINT = "/api/students"


# ===================================
# DATABASE CONNECTION
# ===================================

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

    conn.commit()
    conn.close()


# ===================================
# HOME PAGE
# ===================================

@app.route("/")
def home():
    return render_template("index.html")


# ===================================
# GET ALL STUDENTS
# ===================================

@app.route("/api/students", methods=["GET"])
def get_students():

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ===================================
# GET ONE STUDENT
# ===================================

@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ===================================
# ADD STUDENT
# ===================================

@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        year = int(data["year"])

        if year < 1 or year > 5:
            return jsonify({
                "error": "Year must be between 1 and 5"
            }), 400

        conn = get_db_connection()

        cursor = conn.execute("""
            INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["student_id"].strip(),
            data["name"].strip(),
            data["program"].strip(),
            year,
            data["section"].strip()
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "id": new_id
        }), 201

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid year"}), 400

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


# ===================================
# UPDATE STUDENT
# ===================================

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json(silent=True) or {}

    required_fields = [
        "student_id",
        "name",
        "program",
        "year",
        "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        year = int(data["year"])

        if year < 1 or year > 5:
            return jsonify({
                "error": "Invalid year"
            }), 400

        conn = get_db_connection()

        existing = conn.execute(
            "SELECT id FROM students WHERE id = ?", (id,)
        ).fetchone()

        if existing is None:
            conn.close()
            return jsonify({"error": "Student not found"}), 404

        conn.execute("""
            UPDATE students
            SET student_id = ?,
                name = ?,
                program = ?,
                year = ?,
                section = ?
            WHERE id = ?
        """, (
            data["student_id"].strip(),
            data["name"].strip(),
            data["program"].strip(),
            year,
            data["section"].strip(),
            id
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student updated successfully"
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid year"}), 400

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


# ===================================
# DELETE STUDENT
# ===================================

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?", (id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "message": "Student deleted successfully"
    })


# ===================================
# RETRIEVE CLASSMATE RECORDS
# SERVER-SIDE API REQUEST
# ===================================

@app.route("/partner-records", methods=["GET"])
def partner_records():

    partner_url = CLASSMATE_BASE_URL + CLASSMATE_ENDPOINT

    try:

        response = requests.get(
            partner_url,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            records = data

        elif isinstance(data, dict):
            records = data.get(
                "students",
                data.get("records", [])
            )

        else:
            return jsonify({
                "error": "Invalid classmate API response"
            }), 502

        if not isinstance(records, list):
            return jsonify({
                "error": "Invalid student records format"
            }), 502

        return jsonify(records), 200

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Classmate API request timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Unable to retrieve classmate records",
            "details": str(e)
        }), 502

    except ValueError:
        return jsonify({
            "error": "Classmate API returned invalid JSON"
        }), 502


# ===================================
# RUN FLASK APPLICATION
# ===================================

if __name__ == "__main__":

    init_db()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
