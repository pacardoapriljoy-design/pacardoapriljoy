
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# 1. STUDENT INFORMATION API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2026-00123",
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


# RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)
