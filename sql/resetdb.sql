PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS pantry;
DROP TABLE IF EXISTS user_allergens;
DROP TABLE IF EXISTS user_dietary_prefs;
DROP TABLE IF EXISTS allergens;
DROP TABLE IF EXISTS dietary_prefs;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS pantry_ingredients;
DROP TABLE IF EXISTS meal_calendar_items;
DROP TABLE IF EXISTS meal_calendar_users;

PRAGMA foreign_keys = ON;
