from flask import Flask, render_template, request, redirect
import sqlite3
import webbrowser
from threading import Timer

app = Flask(__name__)

DATABASE = "database/expenses.db"


# -------------------- HOME --------------------

@app.route("/")
def home():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Total Expense
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0]

    if total_expense is None:
        total_expense = 0

    # Total Transactions
    cursor.execute("SELECT COUNT(*) FROM expenses")
    total_transactions = cursor.fetchone()[0]

    # Recent Expenses
    cursor.execute("""
        SELECT amount, category, date, description
        FROM expenses
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_expenses = cursor.fetchall()
    print("Recent Expenses:", recent_expenses)
    conn.close()

    return render_template(
        "index.html",
        total_expense=total_expense,
        total_transactions=total_transactions,
        recent_expenses=recent_expenses
    )


# -------------------- ADD EXPENSE PAGE --------------------

@app.route("/add-expense")
def add_expense():
    return render_template("add_expense.html")


# -------------------- SAVE EXPENSE --------------------

@app.route("/save-expense", methods=["POST"])
def save_expense():

    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]
    description = request.form["description"]

    print("========== FORM DATA ==========")
    print("Amount:", amount)
    print("Category:", category)
    print("Date:", date)
    print("Description:", description)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    """, (amount, category, date, description))

    conn.commit()

    print("Rows inserted:", cursor.rowcount)

    conn.close()
    print("Expense saved successfully!")
    return redirect("/")

# -------------------- EXPENSE HISTORY --------------------

@app.route("/expenses")
def expenses():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return render_template(
        "expense_history.html",
        expenses=expenses
    )


# -------------------- AUTO OPEN BROWSER --------------------

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)