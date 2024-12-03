PRAGMA foreign_keys = ON;

INSERT INTO users(username, first_name, last_name, email, password)
VALUES ('user', 'Shania', 'Twain', 'shatwain@music.com', 
'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO pantry(username, pantry_id)
VALUES('user', 1);

INSERT INTO ingredients(ingredient_name, pantry_id, season, food_group) 
VALUES('Banana', 1, 'summer', 'fruit');