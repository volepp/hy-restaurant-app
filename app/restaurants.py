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
    query = text("INSERT INTO restaurants (name, description, lat, long, created_at) VALUES (:name, :desc, :lat, :lng, :created_at)")
    db.session.execute(query, {
        "name": name,
        "desc": description,
        "lat": lat,
        "lng": lng,
        "created_at": datetime.now()
    })
    db.session.commit()

def validate_restaurant(name, description, lat, long):
    errors = []
    # Name must be 3-20 characters
    if len(name) < 3 or len(name) > 20:
        errors.append("name")
    # Description must be 3-240 characters
    if len(description) < 3 or len(description) > 240:
        errors.append("description")
    if len(lat) == 0 or len(long) == 0:
        errors.append("location")

    return errors

def delete_restaurant(restaurant_id):
    query = text("DELETE FROM restaurants WHERE id=:restaurant_id")
    db.session.execute(query, {"restaurant_id": restaurant_id})
    db.session.commit()

def get_reviews_for_restaurant(restaurant_id):
    query = text("SELECT id, reviewer, stars, comment FROM reviews WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(query, {"restaurant_id": restaurant_id})
    return result.fetchall()

def add_review_for_restaurant(restaurant_id, reviewer, stars, comment):
    query = text("INSERT INTO reviews (restaurant_id, reviewer, stars, comment) VALUES (:restaurant_id, :reviewer, :stars, :comment)")
    db.session.execute(query, {"restaurant_id": restaurant_id, "reviewer": reviewer, "stars": stars, "comment": comment})
    db.session.commit()

def validate_review(stars, comment):
    errors = []
    # Can give only 1-5 stars
    if stars < 1 or stars > 5:
        errors.append("stars")
    # Comment must be 3-240 characters
    if len(comment) < 3 or len(comment) > 240:
        errors.append("comment")
    
    return errors

def get_restaurant_star_avg(restaurant_id):
    query = text("SELECT AVG(stars) AS star_avg FROM reviews WHERE restaurant_id=:restaurant_id")
    result = db.session.execute(query, {"restaurant_id": restaurant_id}).first()
    if result[0] is None:
        return 0
    return float(result[0])

def delete_review(review_id):
    query = text("DELETE FROM reviews WHERE id=:review_id")
    db.session.execute(query, {"review_id": review_id})
    db.session.commit()

def get_all_groups():
    query = text("SELECT id, name FROM groups")
    result = db.session.execute(query)
    return result.fetchall()

def get_group_id_by_name(name):
    query = text("SELECT id FROM groups WHERE name=:name")
    result = db.session.execute(query, {"name": name})
    first = result.first()
    if first is None:
        return -1
    return first[0]

def get_restaurant_groups(restaurant_id):
    query = text("SELECT id, name FROM groups\
                    INNER JOIN restaurants_groups\
                        ON restaurants_groups.restaurant_id = :restaurant_id \
                        AND restaurants_groups.group_id = groups.id")
    result = db.session.execute(query, {"restaurant_id": restaurant_id})
    return result.fetchall()

def restaurant_belongs_to_group(restaurant_id, group_id):
    query = text("SELECT count(*) FROM restaurants_groups WHERE restaurant_id=:restaurant_id AND group_id=:group_id")
    result = db.session.execute(query, {"restaurant_id": restaurant_id, "group_id": group_id})
    count = result.first()[0]
    return count > 0

def create_group(name):
    query = text("INSERT INTO groups (name) VALUES (:name) RETURNING id")
    result = db.session.execute(query, {"name": name})
    db.session.commit()
    new_id = result.first()[0]
    return new_id

def add_restaurant_to_group(restaurant_id, group_id):
    query = text("INSERT INTO restaurants_groups (restaurant_id, group_id) VALUES (:restaurant_id, :group_id)")
    db.session.execute(query, {"restaurant_id": restaurant_id, "group_id": group_id})
    db.session.commit()

def remove_restaurant_from_group(restaurant_id, group_id):
    query = text("DELETE FROM restaurants_groups WHERE restaurant_id=:restaurant_id AND group_id=:group_id")
    db.session.execute(query, {"restaurant_id": restaurant_id, "group_id": group_id})
    db.session.commit()

def validate_group(name):
    errors = []
    # Name must be 3-12 characters
    if len(name) < 3 or len(name) > 12:
        errors.append("name")

    return errors
    