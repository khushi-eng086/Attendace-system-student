import sqlite3


# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Drop existing tables for a clean re-initialization
cursor.execute('DROP TABLE IF EXISTS attendance')
cursor.execute('DROP TABLE IF EXISTS users')

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    role TEXT NOT NULL CHECK(role IN ('Student', 'Faculty'))
)
''')

# Create attendance table
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES users(id)
)
''')

# Insert sample student
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, name, phone, role)
VALUES (?, ?, ?, ?, ?)''', ("john123", "pass123", "John Doe", "1234567890", "Student"))

# Insert sample faculty
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, name, phone, role)
VALUES (?, ?, ?, ?, ?)''', ("faculty1", "admin123", "Prof. Smith", "9876543210", "Faculty"))

# Insert sample attendance for the student
cursor.execute('''
INSERT INTO attendance (student_id, subject, status)
VALUES ((SELECT id FROM users WHERE username = 'john123'), 'Math', 'Present')
''')

cursor.execute('''
INSERT INTO attendance (student_id, subject, status)
VALUES ((SELECT id FROM users WHERE username = 'john123'), 'Science', 'Absent')
''')

# Save changes and close connection
conn.commit()
conn.close()

print("Database initialized with sample data.")