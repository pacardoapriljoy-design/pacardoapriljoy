
import sqlite3
from pathlib import Path

# Get the current project directory
BASE_DIR = Path(__file__).resolve().parent

# Database file
DATABASE = BASE_DIR / "students.db"


def init_db():

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

<<<<<<< HEAD
<<<<<<< HEAD
    # CREATE STUDENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id TEXT NOT NULL UNIQUE,

            name TEXT NOT NULL,

            program TEXT NOT NULL,

            year INTEGER NOT NULL,

            section TEXT NOT NULL

        )
    """)

    # CHECK EXISTING RECORDS
    cursor.execute("SELECT COUNT(*) FROM students")

    count = cursor.fetchone()[0]

    # INSERT DEFAULT STUDENT
    if count == 0:

        cursor.execute("""
            INSERT INTO students
            (student_id, name, program, year, section)

            VALUES (?, ?, ?, ?, ?)

=======
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
            INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
        """, (
            "2026-00001",
            "April Joy Pacardo",
            "BSIT",
            3,
            "Dijkstra"
        ))
=======
        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                program TEXT NOT NULL,
                year INTEGER NOT NULL,
                section TEXT NOT NULL
            )
        """)
>>>>>>> ed01109 (Update Lab 8)

        conn.commit()
        conn.close()

        print("Database initialized successfully!")
        print("Database file:", DATABASE)
        print("Students table created successfully!")

    except sqlite3.Error as e:
        print("Database error:", e)


if __name__ == "__main__":
<<<<<<< HEAD

=======
>>>>>>> f1b37d5 (Complete Laboratory Activity 8)
    init_db()
