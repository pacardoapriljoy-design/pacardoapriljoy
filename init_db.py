import sqlite3

# CONNECT TO DATABASE
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# CREATE STUDENTS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
''')

# CLEAR EXISTING RECORDS
cursor.execute("DELETE FROM students")

# FIVE SAMPLE STUDENT RECORDS
students = [
    ('2026-00001', 'April Joy Pacardo', 'BSIT', 3, 'Dijkstra'),
    ('2026-00002', 'Francine Escultura', 'BSIT', 3, 'Dijkstra'),
    ('2026-00003', 'Jero Paca-oncis', 'BSIT', 2, 'A'),
    ('2026-00004', 'Missy Miranda', 'BSCS', 1, 'B'),
    ('2026-00005', 'Sharmaine Joyce Palencia', 'BSIT', 1, 'A')
]

# INSERT STUDENT RECORDS
cursor.executemany('''
INSERT INTO students
(student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

# SAVE CHANGES
conn.commit()
conn.close()

print("Database created successfully.")
print("Five student records inserted successfully.")
