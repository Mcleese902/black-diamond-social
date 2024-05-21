import sqlite3

connection = sqlite3.connect('users.db')
cursor = connection.cursor()
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
connection.close()

