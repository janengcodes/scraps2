PRAGMA foreign_keys = ON;

INSERT into users (username, fullname, email, password) VALUES
('Emily123', 'Emily Johnson', 'emilyjohnson@email.com', 'mypfp.png', 'password123');

INSERT into recipes (name, ingredient_ids_json, instructions, filename) VALUES 
('Peanut Butter and Jelly Sandwich', '[1,2,3]', '1. Get bread. 
2. Get peanut butter. 3. Get jelly. 4. Put peanut butter on bread. 
5. Put jelly on bread. 6. Put bread together. 7. Eat.', 'pbj.png');

INSERT into recipes (name, ingredient_ids_json, instructions, filename) VALUES 
('Pasta', '[4,5,6]', '1. Cook pasta shells. 2. Drain pasta. 3. Mix pasta with sauce. 4. Eat.', 'pasta.png');

INSERT into recipes (name, ingredient_ids_json, instructions, filename) VALUES 
('Stir Fry', '[7,8,9]', '1. Get vegetables. 2. Fry vegetables on stove. 3. Put sauce. 4. Eat.', 'stirfry.png');

INSERT into ingredients (name) VALUES
('Peanut Butter');

INSERT into ingredients (name) VALUES
('Jelly');

INSERT into ingredients (name) VALUES
('Bread');

INSERT into ingredients (name) VALUES
('Pasta Shells');

INSERT into ingredients (name) VALUES
('Pasta Sauce');

INSERT into ingredients (name) VALUES
('Butter');

INSERT into ingredients (name) VALUES
('Green Bell Pepper');

INSERT into ingredients (name) VALUES
('Onion');

INSERT into ingredients (name) VALUES
('Stir-fry Sauce');