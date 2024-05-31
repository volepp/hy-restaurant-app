CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
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
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id int,
    reviewer TEXT,
    stars INT,
    comment TEXT,

    CONSTRAINT fk_restaurant
        FOREIGN KEY(restaurant_id)
        REFERENCES restaurants(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(reviewer)
        REFERENCES users(username)
        ON DELETE SET NULL
);