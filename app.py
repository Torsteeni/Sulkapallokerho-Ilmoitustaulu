"""Sulkapallokerhon ilmoitustaulu"""
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import forum

app = Flask(__name__)
app.secret_key = config.secret_key


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
def index():
    """Näyttää sovelluksen etusivut"""
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now', 'localtime'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    visits = result[0][0]
    messages = db.query("""
        SELECT m.title, m.content, m.date, u.username, m.id, m.location, m.event_date, m.event_time, m.max_players
        FROM messages m
        left join users u on m.user_id = u.id
        order by m.id desc
    """)
    count = len(messages)
    participants = set()

    if "username" in session:
        user = db.query(
            "SELECT id FROM users WHERE username = ?",
            [session["username"]]
        )

        if user:
            user_id = user[0]["id"]

            registrations = db.query(
                "SELECT message_id FROM participants WHERE user_id = ?",
                [user_id]
            )

            participants = {
                row["message_id"] for row in registrations
            }

    return render_template(
        "mainpage.html",
        count=count,
        visits=visits,
        messages=messages,
        participants=participants
    )

@app.route("/new_message", methods=["GET", "POST"])
@login_required
def thread():
    """Luo uuden ilmoituksen"""
    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        username = session["username"]
        location = request.form["location"]
        event_date = request.form["event_date"]
        event_time = request.form["event_time"]
        players = int(request.form["max_players"])

        user = db.query(
            "SELECT id FROM users WHERE username = ?",
            [username]
        )
        if not user:
            return redirect("/login")

        user_id = user[0][0]

        db.execute("""
            INSERT INTO messages
            (content, user_id, date, title, location,
             event_date, event_time, max_players)
            VALUES (?, ?, datetime('now'), ?, ?, ?, ?, ?)
        """, (content, user_id, title, location,
              event_date, event_time, players))

        return redirect("/")

    return render_template("new_message.html")

@app.route("/enroll/<int:message_id>", methods=["POST"])
@login_required
def enroll(message_id):
    """Ilmoittaa käyttäjän tapahtumaan"""

    if "username" not in session:
        return redirect("/login")

    user = db.query(
        "SELECT id FROM users WHERE username = ?",
        [session["username"]]
    )

    if not user:
        return redirect("/")

    user_id = user[0]["id"]

    message = db.query("""
        SELECT max_players, user_id
        FROM messages
        WHERE id = ?
    """, [message_id])
    
    if message[0]["user_id"] == user_id:
        flash("Et voi ilmoittautua omaan ilmoitukseesi!")
        return redirect(f"/message/{message_id}")
    
    if not message:
        return redirect("/")

    max_players = message[0]["max_players"]

    participants = db.query("""
        SELECT COUNT(*) AS count
        FROM participants
        WHERE message_id = ?
    """, [message_id])

    count = participants[0]["count"]

    already_enrolled = db.query("""
        SELECT id FROM participants
        WHERE user_id = ? AND message_id = ?
    """, [user_id, message_id])

    if already_enrolled:
        return redirect(f"/message/{message_id}")

    if max_players is not None and count >= max_players:
        flash("Tapahtuman ilmoittautumismäärä on täynnä!")
        return redirect(f"/message/{message_id}")

    db.execute(
        """
        INSERT OR IGNORE INTO participants
        (user_id, message_id)
        VALUES (?, ?)
        """,
        [user_id, message_id]
    )

    return redirect(f"/message/{message_id}")

@app.route("/unenroll/<int:message_id>", methods=["POST"])
@login_required
def unenroll(message_id):
    """Poistaa käyttäjän ilmoittautumisen ilmoituksesta."""

    username = session["username"]

    user = db.query("""
        SELECT id FROM users
        WHERE username = ?
    """, [username])

    if not user:
        abort(403)

    user_id = user[0]["id"]

    db.execute("""
        DELETE FROM participants
        WHERE user_id = ? AND message_id = ?
    """, [user_id, message_id])

    return redirect("/message/" + str(message_id))

@app.route("/search")
def search():
    """Hakee käyttäjälle ilmoituksia päivänmäärän perusteella"""
    query = request.args.get("query")

    print("Hakusana:", query)

    results = forum.search(query) if query else []

    print("Hakutulokset:", results)

    return render_template("search.html", query=query, results=results)

@app.route("/message/<int:message_id>")
@login_required
def show_message(message_id):
    """Avaa ilmoituksen sivut"""

    message = db.query("""
        SELECT m.title, m.content, m.date, u.username, m.id, m.location, m.event_date, m.event_time, u.role, m.max_players
        FROM messages m
        left join users u on m.user_id = u.id
        where m.id = ?
    """, [message_id])

    if not message:
        return "Ilmoitusta ei löydy", 404

    participants = db.query("""
        SELECT p.*, u.username
        FROM participants p
        JOIN users u ON p.user_id = u.id
        WHERE p.message_id = ?
    """, [message_id])

    return render_template("message.html", message=message[0], participants=participants)

@app.route("/delete_message/<int:message_id>", methods=["POST"])
@login_required
def delete_message(message_id):
    """Poistaa viestin"""
    db.execute("""
        DELETE FROM messages
        WHERE id = ?
    """, [message_id])
    return redirect("/")

@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    """Käyttäjä voi muokata omaa ilmoitustaan."""

    if "username" not in session:
        return redirect("/login")

    user = db.query(
        "SELECT id FROM users WHERE username = ?",
        [session["username"]]
    )

    if not user:
        return redirect("/")

    user_id = user[0]["id"]

    message = db.query("""
        SELECT *
        FROM messages
        WHERE id = ? AND user_id = ?
    """, [message_id, user_id])

    if not message:
        return "Ilmoitusta ei löydy tai sinulla ei ole oikeutta muokata sitä", 404

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        location = request.form["location"]
        event_date = request.form["event_date"]
        event_time = request.form["event_time"]

        db.execute("""
            UPDATE messages
            SET title = ?,
                content = ?,
                location = ?,
                event_date = ?,
                event_time = ?
            WHERE id = ? AND user_id = ?
        """, [
            title, content, location,
            event_date, event_time,
            message_id, user_id
        ])

        return redirect("/message/" + str(message_id))

    participants = db.query("""
        SELECT p.*, u.username
        FROM participants p
        JOIN users u ON p.user_id = u.id
        WHERE p.message_id = ?
    """, [message_id])

    return render_template(
        "edit_message.html",
        message=message[0],
        participants=participants
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    """Käyttäjä kirjautuu sovellukseen"""
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
        flash("Väärä käyttäjätunnus tai salasana!", "error")
        return redirect("/login")

@app.route("/logout")
def logout():
    """Käyttäjä kirjautuu ulos sovelluksesta"""
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET"])
def register():
    """Käyttäjä rekisteröityy"""
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    """Käyttäjä luo uudet tunnukset"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    role = request.form["role"]

    if password1 != password2:
        flash("Salasanat eivät täsmää!", "error")
        return redirect("/create")

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
        db.execute(sql, [username, password_hash, role])

    except sqlite3.IntegrityError:
        flash("Käyttäjätunnus on jo käytössä!", "error")
        return redirect("/create")

    flash("Tunnus luotu onnistuneesti!", "success")
    return redirect("/login")

