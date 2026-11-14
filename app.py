import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import forum

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now', 'localtime'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    visits = result[0][0]
    messages = db.query("""
        SELECT title, content, date, u.username, m.id 
        FROM messages m
        left join users u on m.user_id = u.id
        order by m.id desc
    """)
    count = len(messages)
    return render_template("mainpage.html", count=count, visits=visits, messages=messages)

@app.route("/new_message", methods=["GET", "POST"])
def thread():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        username = session["username"]

        user = db.query(
            "SELECT id FROM users WHERE username = ?",
            [username]
        )

        user_id = user[0][0]
        db.execute("""
            insert into messages (content, user_id, date, title)
            values (?, ?, datetime('now'), ?)
        """, (content, user_id, title))

        return redirect("/")
    return render_template("new_message.html")

@app.route("/search")
def search():
    query = request.args.get("query")

    print("Hakusana:", query)

    results = forum.search(query) if query else []

    print("Hakutulokset:", results)

    return render_template("search.html", query=query, results=results)

@app.route("/message/<int:message_id>")
def show_message(message_id):
    message = db.query("""
        SELECT m.id, m.title, m.content, m.date, u.username, m.user_id
        FROM messages m
        LEFT JOIN users u ON m.user_id = u.id
        WHERE m.id = ?
    """, [message_id])

    if not message:
        return "Ilmoitusta ei löydy", 404

    return render_template("message.html", message=message[0])

@app.route("/delete_message/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    db.execute("""
        DELETE FROM messages
        WHERE id = ?
    """, [message_id])	
    return redirect("/")

@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    message = db.query("""
        SELECT id, title, content
        FROM messages
        WHERE id = ?
    """, [message_id])

    if not message:
        return "Ilmoitusta ei löydy", 404

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        db.execute("""
            UPDATE messages
            SET title = ?, content = ?
            WHERE id = ?
        """, [title, content, message_id])
        return redirect("/message/" + str(message_id))

    return render_template("edit_message.html", message=message[0])
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
        return render_template("wrong.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return render_template("unmatching.html")

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])

    except sqlite3.IntegrityError:
        return render_template("used.html")

    return redirect("/done")

@app.route("/done")
def done():
	return render_template("done.html")
