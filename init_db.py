
import os
import sqlite3

# ===================================
# DATABASE CONFIGURATION
# ===================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")


# ===================================
# INITIALIZE DATABASE
# ===================================

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

    conn.commit()
    conn.close()

    print("Database initialized successfully!")
    print("Students table is ready!")


# ===================================
# RUN DATABASE INITIALIZATION
# ===================================

if __name__ == "__main__":
    init_db()
