CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT, 
    password TEXT,
    is_admin BOOLEAN    
);
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    lat FLOAT,
    long FLOAT,
    created_at TIMESTAMP
);