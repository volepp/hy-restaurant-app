from app import app
from db import db
import restaurants
from flask import redirect, render_template, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    if "username" not in session:
        return redirect("/login")
    
    search_keyword = request.args.get("restaurantKeyword")
    sort_by = request.args.get("restaurantSortBy")
    if search_keyword is None or search_keyword == "":
        restaurant_list = restaurants.get_restaurants(sort_by=sort_by)
    else:
        restaurant_list = restaurants.get_restaurants_by_keyword(search_keyword, sort_by=sort_by)
        print(restaurant_list)
    
    return render_template("index.html", restaurants=restaurant_list)

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
    is_admin = False
    if "is_admin" in request.form:
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

@app.route("/restaurant/<int:id>")
def restaurant(id):
    if "username" not in session:
        return redirect("/login")
    
    restaurant = restaurants.get_restaurant_by_id(id)
    reviews = restaurants.get_reviews_for_restaurant(id)
    star_avg = round(restaurants.get_restaurant_star_avg(id), 2)
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews, star_average=star_avg)

@app.route("/restaurant", methods=["POST"])
def add_restaurant():
    name = request.form["restaurantName"]
    description = request.form["restaurantDescription"]
    lat = float(request.form["restaurantLatitude"])
    lng = float(request.form["restaurantLongitude"])

    restaurants.create_restaurant(name, description, lat, lng)

    return redirect("/")

@app.route("/restaurant/<int:id>/review", methods=["POST"])
def add_review(id):
    if "username" not in session:
        return redirect("/login")
    reviewer = session["username"]
    stars = request.form["reviewStars"]
    comment = request.form["reviewComment"]

    restaurants.add_review_for_restaurant(id, reviewer, stars, comment)
    return redirect(f"/restaurant/{id}")