
import os
import sqlite3
import requests

from flask import Flask, render_template, request, jsonify
from init_db import init_db, DATABASE


app = Flask(__name__)

# Replace this with your classmate's actual Render URL
CLASSMATE_BASE_URL = os.environ.get(
    "CLASSMATE_BASE_URL",
    "https://francineescultura-4.onrender.com"
)

PARTNER_API = f"{CLASSMATE_BASE_URL}/api/students"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# GET AND CREATE LOCAL STUDENTS
# ==========================================

@app.route("/api/students", methods=["GET", "POST"])
def students():

    if request.method == "GET":

        conn = get_db_connection()

        records = conn.execute("""
            SELECT * FROM students
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        return jsonify([dict(row) for row in records])

    data = request.get_json(silent=True) or {}

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    if not all(data.get(field) not in (None, "") for field in required_fields):
        return jsonify({"error": "All student fields are required"}), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    source = data.get("source", "Local")

    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO students
        (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["student_id"],
        data["name"],
        data["program"],
        year,
        data["section"],
        source
    ))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student saved successfully",
        "id": new_id
    }), 201


# ==========================================
# UPDATE AND DELETE STUDENT
# ==========================================

@app.route("/api/students/<int:student_id>", methods=["PUT", "DELETE"])
def student_detail(student_id):

    conn = get_db_connection()

    existing = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    if request.method == "PUT":

        data = request.get_json(silent=True) or {}

        required_fields = [
            "student_id", "name", "program", "year", "section"
        ]

        if not all(data.get(field) not in (None, "") for field in required_fields):
            conn.close()
            return jsonify({"error": "All student fields are required"}), 400

        try:
            year = int(data["year"])
        except (ValueError, TypeError):
            conn.close()
            return jsonify({"error": "Year must be a number"}), 400

        conn.execute("""
            UPDATE students
            SET student_id = ?,
                name = ?,
                program = ?,
                year = ?,
                section = ?
            WHERE id = ?
        """, (
            data["student_id"],
            data["name"],
            data["program"],
            year,
            data["section"],
            student_id
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Student updated successfully"})

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully"})


# ==========================================
# RETRIEVE PARTNER RECORDS
# ==========================================

@app.route("/partner-records", methods=["GET"])
def partner_records():

    try:
        response = requests.get(
            PARTNER_API,
            timeout=15
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
                "error": "Invalid partner API response"
            }), 502

        if not isinstance(records, list):
            return jsonify({
                "error": "Partner records are not a list"
            }), 502

        return jsonify(records)

    except requests.RequestException as error:

        app.logger.error("Partner API error: %s", error)

        return jsonify({
            "error": "Unable to retrieve partner data"
        }), 502

    except ValueError:

        return jsonify({
            "error": "Partner API returned invalid JSON"
        }), 502


# ==========================================
# IMPORT PARTNER RECORD INTO OWN DATABASE
# ==========================================

@app.route("/import-student", methods=["POST"])
def import_student():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    if not all(data.get(field) not in (None, "") for field in required_fields):
        return jsonify({
            "error": "Incomplete student record"
        }), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid year"}), 400

    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO students
        (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["student_id"],
        data["name"],
        data["program"],
        year,
        data["section"],
        "Classmate API"
    ))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Remote record saved successfully",
        "id": new_id,
        "source": "Classmate API"
    }), 201


# ==========================================
# SEND PRACTICE RECORD TO PARTNER
# ==========================================

@app.route("/send-to-partner", methods=["POST"])
def send_to_partner():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    if not all(data.get(field) not in (None, "") for field in required_fields):
        return jsonify({
            "error": "All student fields are required"
        }), 400

    try:
        record = {
            "student_id": data["student_id"],
            "name": data["name"],
            "program": data["program"],
            "year": int(data["year"]),
            "section": data["section"],
            "source": "Partner API"
        }
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid year"}), 400

    try:
        response = requests.post(
            PARTNER_API,
            json=record,
            timeout=15
        )

        response.raise_for_status()

        return jsonify({
            "message": "Record sent successfully to partner",
            "partner_response": response.json()
        }), 200

    except requests.RequestException as error:

        app.logger.error("Sending to partner failed: %s", error)

        return jsonify({
            "error": "Unable to send record to partner",
            "details": str(error)
        }), 502


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    init_db()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
