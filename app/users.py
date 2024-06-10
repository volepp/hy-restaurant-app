from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy import text

def get_user(username):
    query = text("SELECT id, password, is_admin FROM users WHERE username=:username")
    result = db.session.execute(query, {"username": username})
    return result.fetchone()

def is_valid_password(user, password):
    pw_hash = user.password
    if check_password_hash(pw_hash, password):
        return True
    return False

def create_user(username, password, is_admin):
    pw_hash = generate_password_hash(password)
    query = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)")
    db.session.execute(query, {"username": username, "password": pw_hash, "is_admin": is_admin})
    db.session.commit()

def validate_user(username, password):
    errors = []
    # Username must be 3-20 characters
    if len(username) < 3 or len(username) > 20:
        errors.append("username")
    
    # Password must be 3-20 characters
    if len(password) < 3 or len(password) > 20:
        errors.append("password")
    
    return errors