import sqlite3

connection = sqlite3.connect('black_diamond_social.db')
cursor = connection.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Create user_profiles table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id INTEGER PRIMARY KEY,
    profile_picture TEXT,
    bio TEXT,
    signature TEXT,
    social_links TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Create status_updates table
cursor.execute("""
CREATE TABLE IF NOT EXISTS status_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Create friends table
cursor.execute("""
CREATE TABLE IF NOT EXISTS friends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    friend_id INTEGER,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(friend_id) REFERENCES users(id)
)
""")

# Create coworkers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS coworkers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    coworker_id INTEGER,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(coworker_id) REFERENCES users(id)
)
""")

# Create tasks table
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

