PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    password VARCHAR(40) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE pantry(
    username VARCHAR(20) NOT NULL,
    pantry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    FOREIGN KEY(username)
        REFERENCES users(username)
        ON DELETE CASCADE
);

CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL,
    name VARCHAR(64) NOT NULL,
    instructions JSON
);

CREATE TABLE ingredients(
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name VARCHAR(64),
    pantry_id INTEGER,
    season VARCHAR(64) CHECK (season IN ('spring', 'summer', 'fall', 'winter')),
    food_group VARCHAR(64) CHECK (food_group IN ('protein', 'produce', 'dairy', 'grains', 'fruit', 'veggies')),
    FOREIGN KEY (pantry_id) REFERENCES pantry (pantry_id)
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER NOT NULL, 
    ingredient_id INTEGER NOT NULL,
    quantity TEXT, 
    unit VARCHAR(40),

    FOREIGN KEY(recipe_id)
        REFERENCES recipes(recipe_id)
        ON DELETE CASCADE,
    FOREIGN KEY(ingredient_id) 
        REFERENCES ingredients(ingredient_id)
        ON DELETE CASCADE

    CONSTRAINT unique_recipe_ingredient UNIQUE (recipe_id, ingredient_id)
);

CREATE TABLE pantry_ingredients (
    pantry_id INTEGER NOT NULL, 
    ingredient_id INTEGER NOT NULL,

    FOREIGN KEY(pantry_id)
        REFERENCES pantry(pantry_id)
        ON DELETE CASCADE,
    FOREIGN KEY(ingredient_id)
        REFERENCES ingredients(ingredient_id)
        ON DELETE CASCADE,

    CONSTRAINT unique_pantry_ingredient UNIQUE (pantry_id, ingredient_id)
);

