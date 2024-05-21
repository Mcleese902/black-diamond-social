import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection to an SQLite database"""
    try:
        connection = sqlite3.connect('black_diamond_therapy.db')
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_user_table():
    """Create the users table"""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.close()