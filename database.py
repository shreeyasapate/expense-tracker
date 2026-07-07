import sqlite3

connection = sqlite3.connect("database/expenses.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")