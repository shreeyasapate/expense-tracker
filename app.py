from flask import Flask, render_template, request, redirect
import sqlite3
import webbrowser
from threading import Timer
app = Flask(__name__)

DATABASE = "database/expenses.db"

@app.route("/")
def home():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0]

    if total_expense is None:
        total_expense = 0

    # Count total transactions
    cursor.execute("SELECT COUNT(*) FROM expenses")
    total_transactions = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total_expense=total_expense,
        total_transactions=total_transactions
    )


@app.route("/add-expense")
def add_expense():
    return render_template("add_expense.html")


@app.route("/save-expense", methods=["POST"])
def save_expense():

    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]
    description = request.form["description"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    """, (amount, category, date, description))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/expenses")
def expenses():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    conn.close()

    return render_template("expense_history.html", expenses=expenses)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")
    
if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
    