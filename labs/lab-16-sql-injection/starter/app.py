"""
Lab 16 — SQL Injection
Starter: Vulnerable login app

Run with:
    pip install flask
    python app.py

Then visit http://localhost:5000
"""

import sqlite3
import os
from flask import Flask, request, g, render_template_string

app = Flask(__name__)
DATABASE = "users.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Create the users table and seed two accounts."""
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)
        db.execute("""
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES ('admin', 'supersecret', 'admin')
        """)
        db.execute("""
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES ('alice', 'hunter2', 'user')
        """)
        db.commit()


LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Lab 16 — Login</title></head>
<body>
  <h1>Login</h1>
  {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
  <form method="POST" action="/login">
    <label>Username: <input type="text" name="username"></label><br><br>
    <label>Password: <input type="password" name="password"></label><br><br>
    <button type="submit">Login</button>
  </form>
  <hr>
  <small>Hint: there are two accounts — admin and alice.</small>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Lab 16 — Dashboard</title></head>
<body>
  <h1>Welcome, {{ username }}!</h1>
  <p>Role: <strong>{{ role }}</strong></p>
  <p>You are logged in.</p>
  <a href="/">Log out</a>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(LOGIN_PAGE, error=None)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    db = get_db()

    # TODO (Exercise 5 — PATCH): replace this vulnerable query with a
    # parameterized query. Do not change anything else.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = db.execute(query).fetchone()

    if user:
        return render_template_string(
            DASHBOARD_PAGE, username=user["username"], role=user["role"]
        )
    else:
        return render_template_string(LOGIN_PAGE, error="Invalid credentials"), 401


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    else:
        init_db()
    app.run(debug=True, port=5000)
