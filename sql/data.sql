PRAGMA foreign_keys = ON;

INSERT INTO users(username, first_name, last_name, email, password)
VALUES ('user', 'Shania', 'Twain', 'shatwain@music.com', 
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO pantry(username, pantry_id)
VALUES('user', 1);

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Apple', 'fall', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Apricot', 'spring', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Cherry', 'spring', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Cranberry', 'fall', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Fig', 'fall', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Grapefruit', 'winter', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Kumquat', 'winter', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Lemon', 'spring', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Peach', 'summer', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Persimmon', 'winter', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Strawberry', 'summer', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Watermelon', 'summer', 'fruit');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Arugula', 'spring', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Bell Pepper', 'summer', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Broccoli', 'fall', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Cabbage', 'winter', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Carrot', 'winter', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Chili', 'summer', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Eggplant', 'summer', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Kale', 'spring', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Lettuce', 'spring', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Spinach', 'winter', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Squash', 'fall', 'veggies');

INSERT INTO ingredients(ingredient_name, season, food_group)
VALUES('Turnip', 'fall', 'veggies');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Butter', 'dairy');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Condensed Milk', 'dairy');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Heavy Cream', 'dairy');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Milk', 'dairy');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Sour Cream', 'dairy');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Yogurt', 'dairy');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Bacon', 'protein');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Chicken Breast', 'protein');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Ground Beef', 'protein');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Salmon', 'protein');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Shrimp', 'protein');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Tofu', 'protein');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Bread', 'grains');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Corn', 'grains');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Oats', 'grains');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Pasta', 'grains');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Quinoa', 'grains');

INSERT INTO ingredients(ingredient_name, food_group)
VALUES('Rice', 'grains');

