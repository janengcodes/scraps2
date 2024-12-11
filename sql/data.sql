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

