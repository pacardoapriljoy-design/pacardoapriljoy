from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to April Joy Pacardo's API!"

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "YOUR STUDENT ID",
        "name": "April Joy Pacardo",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'April Joy Pacardo')
    return jsonify({
        "message": f"Hello, {name}!"
    })

# New Endpoint 1: Student Profile
@app.route('/profile')
def profile():
    return jsonify({
        "name": "April Joy Pacardo",
        "course": "Bachelor of Science in Information Technology",
        "year_level": 3,
        "section": "B",
        "status": "Currently Enrolled"
    })

# New Endpoint 2: Study Goal
@app.route('/study-goal')
def study_goal():
    goal = request.args.get('goal', 'Learn Python programming')
    return jsonify({
        "student": "April Joy Pacardo",
        "study_goal": goal,
        "message": f"My study goal is to {goal}."
    })

if __name__ == '__main__':
    app.run(debug=True)