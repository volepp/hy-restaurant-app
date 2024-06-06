from db import db
from sqlalchemy import text, select, func, or_
from datetime import datetime

def get_restaurants(sort_by=None):
    sort_query = format_sort_by_query(sort_by)
    query = text(f"\
                 SELECT restaurants.id, restaurants.name, restaurants.description, restaurants.lat, restaurants.long, AVG(COALESCE(reviews.stars, 0)) AS star_average \
                 FROM restaurants \
                 LEFT JOIN reviews ON restaurants.id = reviews.restaurant_id\
                 GROUP BY restaurants.id \
                 {sort_query}")
    print(query)
    result = db.session.execute(query)
    return result.fetchall()

def get_restaurants_by_keyword(keyword, sort_by=None):
    sort_query = format_sort_by_query(sort_by)
    query = text(f"\
                SELECT restaurants.id, restaurants.name, restaurants.description, restaurants.lat, restaurants.long, AVG(COALESCE(reviews.stars, 0)) AS star_average \
                 FROM restaurants \
                 LEFT JOIN reviews ON restaurants.id = reviews.restaurant_id\
                 WHERE UPPER(restaurants.name) LIKE UPPER(:keyword) OR UPPER(restaurants.description) LIKE UPPER(:keyword)\
                 GROUP BY restaurants.id \
                 {sort_query}")
    result = db.session.execute(query, {"keyword": f"%{keyword}%"})
    return result.fetchall()

def format_sort_by_query(sort_by):
    if sort_by == "alphabetical_asc":
        return "ORDER BY restaurants.name ASC"
    elif sort_by == "alphabetical_desc":
        return "ORDER BY restaurants.name DESC"
    elif sort_by == "rating_asc":
        return "ORDER BY star_average ASC"
    elif sort_by == "rating_desc":
        return "ORDER BY star_average DESC"
    return ""

def get_restaurant_by_id(id):
    query = text("SELECT * FROM restaurants WHERE id=:id")
    result = db.session.execute(query, {"id": id})
    return result.fetchone()

def create_restaurant(name, description, lat, lng):
    # TODO validate fields
    query = text("INSERT INTO restaurants (name, description, lat, long, created_at) VALUES (:name, :desc, :lat, :lng, :created_at)")
    db.session.execute(query, {
        "name": name,
        "desc": description,
        "lat": lat,
        "lng": lng,
        "created_at": datetime.now()
    })
    db.session.commit()

def get_reviews_for_restaurant(restaurant_id):
    query = text("SELECT reviewer, stars, comment FROM reviews WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(query, {"restaurant_id": restaurant_id})
    return result.fetchall()

def add_review_for_restaurant(restaurant_id, reviewer, stars, comment):
    # TODO: validate stars and comment
    query = text("INSERT INTO reviews (restaurant_id, reviewer, stars, comment) VALUES (:restaurant_id, :reviewer, :stars, :comment)")
    db.session.execute(query, {"restaurant_id": restaurant_id, "reviewer": reviewer, "stars": stars, "comment": comment})
    db.session.commit()

def get_restaurant_star_avg(restaurant_id):
    query = text("SELECT AVG(stars) AS star_avg FROM reviews WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(query, {"restaurant_id": restaurant_id}).first()
    if result[0] is None:
        return 0
    return float(result[0])

def delete_restaurant(restaurant_id):
    query = text("DELETE FROM restaurants WHERE id=:restaurant_id")
    db.session.execute(query, {"restaurant_id": restaurant_id})
    db.session.commit()