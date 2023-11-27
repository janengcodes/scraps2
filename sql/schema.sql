CREATE TABLE users(
    username VARCHAR(20) NOT NULL,  /* VARCHAR means it can be any number of characters up to the num in parenthesis */
    fullname VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    filename VARCHAR(64) NOT NULL,
    password VARCHAR(40) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username)
);

CREATE TABLE recipes(
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    filename VARCHAR(64) NOT NULL,
    ingredient_ids_json TEXT NOT NULL, /* JSON data */
    instructions TEXT NOT NULL,
    cook_time INT NOT NULL /* in minutes */
);

CREATE TABLE saved_recipes(
    username VARCHAR(20) NOT NULL,
    recipe_id INTEGER NOT NULL,
    meal_time TEXT CHECK (meal_time IN ('breakfast', 'lunch', 'dinner')),

    FOREIGN KEY(username)
        REFERENCES users(username)
        ON DELETE CASCADE,

    FOREIGN KEY(recipe_id)
        REFERENCES recipes(recipe_id)
        ON DELETE CASCADE
);

CREATE TABLE ingredients(
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL
    /* TODO: Add more metadata */
);

CREATE TABLE pantry(
    username VARCHAR(20) NOT NULL,
    ingredient_id INTEGER NOT NULL,
    
    FOREIGN KEY(username)
        REFERENCES users(username)
        ON DELETE CASCADE
);

CREATE TABLE calendar_events(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    meal_time TEXT CHECK (meal_time IN ('breakfast', 'lunch', 'dinner')),
    
    FOREIGN KEY(username)
        REFERENCES users(username)
        ON DELETE CASCADE,
    
    FOREIGN KEY(recipe_id)
        REFERENCES recipes(recipe_id)
        ON DELETE CASCADE
);
