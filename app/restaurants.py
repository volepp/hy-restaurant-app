from db import db
from sqlalchemy import text
from datetime import datetime

def get_restaurants():
    query = text("SELECT name, description, lat, long FROM restaurants")
    result = db.session.execute(query)
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