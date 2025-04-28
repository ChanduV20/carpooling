from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn


def close_db(conn):
    if conn:
        conn.close()

conn = get_db()
cursor = conn.cursor()
# cursor.execute('delete from users where username = "Sandeep_J3" ')
rows = cursor.execute("SELECT username,src,dst FROM users").fetchall()
wh = [{"username":row["username"] , "src": row["src"], "dst": row["dst"]} for row in rows]
print(wh)
close_db(conn)
