import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database and expenses table created successfully!")