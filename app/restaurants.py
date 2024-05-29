from db import db
from sqlalchemy import text, select, or_
from datetime import datetime

def get_restaurants():
    query = text("SELECT name, description, lat, long FROM restaurants")
    result = db.session.execute(query)
    return result.fetchall()

def get_restaurants_by_keyword(keyword):
    # query = text("""SELECT name, description, lat, long FROM restaurants
    #               WHERE name LIKE :keyword
    #               OR description LIKE :keyword""")
    query = select(text("name, description, lat, long"))\
            .where(
                or_(
                        text("name LIKE :keyword"),
                        text("description LIKE :keyword")
                )
            ).select_from(text("restaurants"))
    print(query)
    result = db.session.execute(query, {"keyword": f"%{keyword}%"})
    return result.fetchall()

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