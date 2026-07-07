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


    # Expense By Category
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    category_data = cursor.fetchall()


    # Monthly Expense Data
    cursor.execute("""
        SELECT strftime('%Y-%m', date), SUM(amount)
        FROM expenses
        GROUP BY strftime('%Y-%m', date)
        ORDER BY date
    """)
    monthly_data = cursor.fetchall()


    conn.close()


    return render_template(
        "index.html",
        total_expense=total_expense,
        total_transactions=total_transactions,
        recent_expenses=recent_expenses,
        category_data=category_data,
        monthly_data=monthly_data
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


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO expenses
        (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    """,
    (amount, category, date, description))


    conn.commit()
    conn.close()


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



# -------------------- EDIT EXPENSE --------------------

@app.route("/edit-expense/<int:id>")
def edit_expense(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
    """,
    (id,))


    expense = cursor.fetchone()


    conn.close()


    return render_template(
        "edit_expense.html",
        expense=expense
    )



# -------------------- UPDATE EXPENSE --------------------

@app.route("/update-expense/<int:id>", methods=["POST"])
def update_expense(id):

    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]
    description = request.form["description"]


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
        UPDATE expenses
        SET amount = ?,
            category = ?,
            date = ?,
            description = ?
        WHERE id = ?
    """,
    (
        amount,
        category,
        date,
        description,
        id
    ))


    conn.commit()
    conn.close()


    return redirect("/expenses")



# -------------------- DELETE EXPENSE --------------------

@app.route("/delete-expense/<int:id>")
def delete_expense(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """,
    (id,))


    conn.commit()
    conn.close()


    return redirect("/expenses")



# -------------------- AUTO OPEN BROWSER --------------------

def open_browser():

    webbrowser.open_new(
        "http://127.0.0.1:5000/"
    )



# -------------------- RUN APP --------------------

if __name__ == "__main__":

    Timer(1, open_browser).start()

    app.run(
        debug=True,
        use_reloader=False
    )