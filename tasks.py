import sqlite3

connection = sqlite3.connect('black_diamond_social.db')
cursor = connection.cursor()

# Update user_profiles table to include 'signature' column if it doesn't exist
cursor.execute("PRAGMA table_info(user_profiles)")
columns = [column[1] for column in cursor.fetchall()]

if 'signature' not in columns:
    cursor.execute("ALTER TABLE user_profiles ADD COLUMN signature TEXT")

# Ensure tasks table includes user_id to associate tasks with specific users
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT NOT NULL,
    details TEXT,
    category TEXT,
    due_date TEXT,
    priority TEXT,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

connection.commit()
connection.close()

