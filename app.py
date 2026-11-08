
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00065",
        "name": "April Joy Pacardo",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# CUSTOM API: MY STUDENT PROFILE
@app.route('/my-profile')
def my_profile():
    return jsonify({
        "student_id": "24-00065",
        "name": "April Joy Pacardo",
        "program": "BSIT",
        "year": 3,
        "section": "DIJKSTRA",
        "favorite_language": "Python",
        "hobby": "Learning programming",
        "goal": "Become a successful IT professional"
    })

if __name__ == '__main__':
    app.run(debug=True)
