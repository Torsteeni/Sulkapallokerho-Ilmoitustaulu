import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now', 'localtime'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    count = result[0][0]
    return render_template("mainpage.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("index.html")

    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if result and check_password_hash(result[0][0], password):
        session["username"] = username
        return redirect("/")

    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
   
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return redirect("/done")

@app.route("/done")
def done():
	return render_template("done.html")
