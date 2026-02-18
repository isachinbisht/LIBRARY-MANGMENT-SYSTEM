from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = "library_secret"


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Disha@10",  
        database="library_db"
    )


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/loading")

        return "Invalid Credentials"

    return render_template("index.html")


@app.route("/loading")
def loading():
    return render_template("loading.html")


@app.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("dashboard.html", books=books)


@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("books.html", books=books)


@app.route("/add_book", methods=["POST"])
def add_book():
    if session.get("role") != "admin":
        return redirect("/")

    title = request.form["title"]
    author = request.form["author"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author) VALUES (%s, %s)",
        (title, author)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/dashboard")


@app.route("/issue/<int:book_id>")
def issue_book(book_id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO issued_books (book_id, student_id, issue_date) VALUES (%s, %s, %s)",
        (book_id, session["user_id"], date.today())
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/books")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
