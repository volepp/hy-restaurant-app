from app import app
from db import db
from flask import redirect, render_template, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    if "username" not in session:
        return redirect("/login")

    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    
    query = text("SELECT id, password, is_admin FROM users WHERE username=:username")
    result = db.session.execute(query, {"username": username})
    user = result.fetchone()
    if not user:
        # TODO: Invalid username
        pass
    else:
        pw_hash = user.password
        if check_password_hash(pw_hash, password):
            session["username"] = username
            session["is_admin"] = user.is_admin
            return redirect("/")
        else:
            # TODO: Invalid password
            pass

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    username = request.form["username"]
    password = request.form["password"]
    is_admin = request.form["is_admin"] == "on"

    pw_hash = generate_password_hash(password)
    query = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)")
    db.session.execute(query, {"username": username, "password": pw_hash, "is_admin": is_admin})
    db.session.commit()

    session["username"] = username
    session["is_admin"] = is_admin
    return redirect("/")

@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
    return redirect("/")