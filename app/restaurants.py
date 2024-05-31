from db import db
from sqlalchemy import text, select, func, or_
from datetime import datetime

def get_restaurants():
    query = text("\
                 SELECT restaurants.id, restaurants.name, restaurants.description, restaurants.lat, restaurants.long, AVG(reviews.stars) AS star_average \
                 FROM restaurants \
                 LEFT JOIN reviews ON restaurants.id = reviews.restaurant_id\
                 GROUP BY restaurants.id")
    result = db.session.execute(query)
    return result.fetchall()

def get_restaurants_by_keyword(keyword):
    query = text("\
                SELECT restaurants.id, restaurants.name, restaurants.description, restaurants.lat, restaurants.long, AVG(reviews.stars) AS star_average \
                 FROM restaurants \
                 LEFT JOIN reviews ON restaurants.id = reviews.restaurant_id\
                 WHERE restaurants.name LIKE :keyword OR restaurants.description LIKE :keyword\
                 GROUP BY restaurants.id")
    result = db.session.execute(query, {"keyword": f"%{keyword}%"})
    return result.fetchall()

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