CREATE TABLE users(
    username VARCHAR(20) NOT NULL,  /* VARCHAR means it can be any number of characters up to the num in parenthesis */
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    password VARCHAR(40) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE recipes(
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    ingredients_json TEXT NOT NULL,
    measurements_json TEXT NOT NULL,
    instructions TEXT NOT NULL,
    serving_size INTEGER NOT NULL,
    cook_time INTEGER NOT NULL,
    prep_time INTEGER NOT NULL
);

CREATE TABLE saved_recipes(
    username VARCHAR(20) NOT NULL,
    recipe_id INTEGER NOT NULL,

    FOREIGN KEY(username)
        REFERENCES users(username)
        ON DELETE CASCADE,

    FOREIGN KEY(recipe_id)
        REFERENCES recipes(recipe_id)
        ON DELETE CASCADE
);

CREATE TABLE ingredients(
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    pantry_id INTEGER,

    season VARCHAR(64) CHECK (season IN ('spring', 'summer', 'fall', 'winter')) NOT NULL,
    food_group VARCHAR(64) CHECK (food_group IN ('meat', 'fruit', 'veggies', 'grains')) NOT NULL,

    FOREIGN KEY(pantry_id)
        REFERENCES pantry(pantry_id)
);


CREATE TABLE pantry(
    username VARCHAR(20) NOT NULL,
    pantry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    FOREIGN KEY(username)
        REFERENCES users(username)
        ON DELETE CASCADE
);

