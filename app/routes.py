from app import app
from db import db
import restaurants
import users
from flask import redirect, render_template, abort, request, session, Response
from sqlalchemy import text

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

    return render_template("index.html", restaurants=restaurant_list)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    
    user = users.get_user(username)
    if not user:
        return redirect("/login?error=true")
    elif users.is_valid_password(user, password):
        session["username"] = username
        session["is_admin"] = user.is_admin
        return redirect("/")
    else:
        # Invalid password
        return redirect("/login?error=true")

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

    validation_errors = users.validate_user(username, password)
    if len(validation_errors) > 0:
        err_str = ",".join(validation_errors)
        return redirect(f"/register?errors={err_str}")
    users.create_user(username, password, is_admin)

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
    groups = restaurants.get_restaurant_groups(id)
    all_groups = restaurants.get_all_groups()
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews, star_average=star_avg, groups=groups, all_groups=all_groups)

@app.route("/restaurant", methods=["POST"])
def add_restaurant():
    name = request.form["restaurantName"]
    description = request.form["restaurantDescription"]
    lat_str = request.form["restaurantLatitude"]
    lng_str = request.form["restaurantLongitude"]

    validation_errors = restaurants.validate_restaurant(name, description, lat_str, lng_str)
    if len(validation_errors) > 0:
        err_str = ",".join(validation_errors)
        return redirect(f"/?addErrors={err_str}")
    
    lat = float(lat_str)
    lng = float(lng_str)

    restaurants.create_restaurant(name, description, lat, lng)

    return redirect("/")

@app.route("/restaurant/<int:id>/delete", methods=["POST"])
def delete_restaurant(id):
    if "is_admin" not in session or session["is_admin"] == False:
        abort(401)
    
    restaurants.delete_restaurant(id)
    return redirect("/")

@app.route("/restaurant/<int:id>/review", methods=["POST"])
def add_review(id):
    if "username" not in session:
        return redirect("/login")
    reviewer = session["username"]
    stars = int(request.form["reviewStars"])
    comment = request.form["reviewComment"]

    validation_errors = restaurants.validate_review(stars, comment)
    if len(validation_errors) > 0:
        err_str = ",".join(validation_errors)
        return redirect(f"/restaurant/{id}?reviewErrors={err_str}")

    restaurants.add_review_for_restaurant(id, reviewer, stars, comment)
    return redirect(f"/restaurant/{id}")

@app.route("/restaurant/<int:restaurant_id>/review/<int:review_id>/delete", methods=["POST"])
def delete_review(restaurant_id, review_id):
    if "is_admin" not in session or session["is_admin"] == False:
        abort(401)
    
    restaurants.delete_review(review_id)
    return redirect(f"/restaurant/{restaurant_id}")

@app.route("/restaurant/<int:restaurant_id>/groups/new", methods=["POST"])
def add_new_group(restaurant_id):
    if "is_admin" not in session or session["is_admin"] == False:
        abort(401)

    name = request.form["newGroupName"]
    validation_errors = restaurants.validate_group(name)
    if len(validation_errors) > 0:
        return redirect(f"/restaurant/{restaurant_id}")
    
    new_group_id = restaurants.create_group(name)
    restaurants.add_restaurant_to_group(restaurant_id, new_group_id)
    return redirect(f"/restaurant/{restaurant_id}")

@app.route("/restaurant/<int:restaurant_id>/groups/existing", methods=["POST"])
def add_existing_group(restaurant_id):
    if "is_admin" not in session or session["is_admin"] == False:
        abort(401)
        
    existing_group_name = request.form["existingGroupName"]
    group_id = restaurants.get_group_id_by_name(existing_group_name)
    if group_id == -1:
        # Group not found
        return redirect(f"/restaurant/{restaurant_id}")

    if not restaurants.restaurant_belongs_to_group(restaurant_id, group_id):
        restaurants.add_restaurant_to_group(restaurant_id, group_id)

    return redirect(f"/restaurant/{restaurant_id}")

@app.route("/restaurant/<int:restaurant_id>/groups/remove", methods=["POST"])
def remove_group(restaurant_id):
    if "is_admin" not in session or session["is_admin"] == False:
        abort(401)

    group_name = request.form["deleteGroupName"]
    group_id = restaurants.get_group_id_by_name(group_name)
    if group_id == -1:
        # Group not found
        return redirect(f"/restaurant/{restaurant_id}")
    
    restaurants.remove_restaurant_from_group(restaurant_id, group_id)
    return redirect(f"/restaurant/{restaurant_id}")

@app.errorhandler(401)
def custom_401(error):
    return Response("Unauthorized", 401, {'WWW-Authenticate':'Basic realm="Login Required"'})