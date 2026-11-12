import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Your classmate's Render API endpoint
CLASSMATE_API = "https://francineescultura-4.onrender.com/api/students"

# Simulated local database (replace with SQLAlchemy / SQLite / MySQL in your real app)
local_students = [
    {
        "id": 1,
        "student_id": "2026-00001",
        "name": "Juan Dela Cruz",
        "program": "BSIT",
        "year": 3,
        "section": "A",
        "source": "Local"
    }
]


# ---------------------------------------------------------
# 1. FETCH FROM CLASSMATE API (Replaces Local-only view)
# ---------------------------------------------------------
def fetch_classmate_students():
    try:
        # Timeout set to 60s because Render free-tier servers sleep when idle
        response = requests.get(CLASSMATE_API, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Normalize records so they match your table columns & badge
        formatted = []
        for idx, item in enumerate(data, start=100):
            formatted.append({
                "id": item.get("id", idx),
                "student_id": item.get("student_id", ""),
                "name": item.get("name", ""),
                "program": item.get("program", ""),
                "year": item.get("year", ""),
                "section": item.get("section", ""),
                "source": "Classmate API"  # Forces the purple badge label
            })
        return formatted

    except requests.RequestException as e:
        print(f"Error fetching from Classmate API: {e}")
        return []


# ---------------------------------------------------------
# 2. PUSH A STUDENT TO CLASSMATE API (POST)
# ---------------------------------------------------------
def push_to_classmate(student_data):
    payload = {
        "student_id": student_data["student_id"],
        "name": student_data["name"],
        "program": student_data["program"],
        "year": int(student_data["year"]),
        "section": student_data["section"],
        "source": "Classmate API"
    }
    try:
        response = requests.post(CLASSMATE_API, json=payload, timeout=60)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as e:
        return False, str(e)


# ---------------------------------------------------------
# 3. WEB ROUTE: DISPLAY CLASSMATE STUDENTS IN TABLE
# ---------------------------------------------------------
@app.route("/")
def index():
    # Fetch directly from Classmate API instead of local_students
    students = fetch_classmate_students()
    
    # Optional: If you want BOTH local and classmate records combined, uncomment below:
    # students = local_students + fetch_classmate_students()

    return render_template_string(HTML_TEMPLATE, students=students)


# ---------------------------------------------------------
# 4. API ENDPOINT: ALLOW CLASSMATE TO POST TO YOUR APP
# ---------------------------------------------------------
@app.route("/api/students", methods=["GET", "POST"])
def api_students():
    if request.method == "GET":
        return jsonify(local_students), 200

    if request.method == "POST":
        data = request.get_json()
        new_record = {
            "id": len(local_students) + 1,
            "student_id": data.get("student_id"),
            "name": data.get("name"),
            "program": data.get("program"),
            "year": data.get("year"),
            "section": data.get("section"),
            "source": "Classmate API"  # Marks incoming POSTs as Classmate API
        }
        local_students.append(new_record)
        return jsonify({"message": "Synced successfully", "record": new_record}), 201


# ---------------------------------------------------------
# 5. HTML TABLE TEMPLATE (Matches your UI)
# ---------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Records</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th { background-color: #ede9fe; color: #5b21b6; text-align: left; padding: 12px; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        .badge {
            background-color: #f3e8ff;
            color: #7e22ce;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 12px;
        }
        .btn-edit { background: #7c3aed; color: white; border: none; padding: 6px 12px; border-radius: 6px; }
        .btn-delete { background: #e11d48; color: white; border: none; padding: 6px 12px; border-radius: 6px; }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Student ID</th>
                <th>Name</th>
                <th>Program</th>
                <th>Year</th>
                <th>Section</th>
                <th>Source</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for s in students %}
            <tr>
                <td>{{ s.id }}</td>
                <td>{{ s.student_id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.program }}</td>
                <td>{{ s.year }}</td>
                <td>{{ s.section }}</td>
                <td><span class="badge">{{ s.source }}</span></td>
                <td>
                    <button class="btn-edit">Edit</button>
                    <button class="btn-delete">Delete</button>
                </td>
            </tr>
            {% else %}
            <tr><td colspan="8">No records found from Classmate API.</td></tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
