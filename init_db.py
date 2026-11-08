
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "students.db"


def init_db():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

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


if __name__ == "__main__":
    init_db()
