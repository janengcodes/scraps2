PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    password VARCHAR(40) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE dietary_preferences (
    dietary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dietary_name VARCHAR(40) NOT NULL
);

CREATE TABLE allergens (
    allergen_id INTEGER PRIMARY KEY AUTOINCREMENT,
    allergen_name VARCHAR(40) NOT NULL
);

CREATE TABLE user_diet_pref (
    username VARCHAR(20) NOT NULL,
    dietary_id INTEGER NOT NULL,
    PRIMARY KEY(username, dietary_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(dietary_id) REFERENCES dietary_preferences(dietary_id)
);

CREATE TABLE user_allergens (
    username VARCHAR(20) NOT NULL,
    allergen_id INTEGER NOT NULL,
    PRIMARY KEY(username, allergen_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(allergen_id) REFERENCES allergens(allergen_id)
);

CREATE TABLE dietary_prefs (
    dietary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dietary_name VARCHAR(40) NOT NULL
);

CREATE TABLE user_dietary_prefs (
    username VARCHAR(20) NOT NULL,
    dietary_id INTEGER NOT NULL,
    PRIMARY KEY(username, dietary_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(dietary_id) REFERENCES dietary_prefs(dietary_id)
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
    username VARCHAR(20),
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

CREATE TABLE meal_calendar_users (
    meal_calendar_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
        ON DELETE CASCADE
);

CREATE TABLE meal_calendar_item (
    meal_calendar_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_calendar_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    recipe_link VARCHAR(40),
    meal_type VARCHAR(40),
    meal_name VARCHAR(40),
    meal_day VARCHAR(40) CHECK (meal_day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY(meal_calendar_id) REFERENCES meal_calendar_users(meal_calendar_id)
        ON DELETE CASCADE
);

