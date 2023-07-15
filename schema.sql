




















CREATE TABLE users(id SERIAL PRIMARY KEY, name VARCHAR(50), email TEXT NOT NULL UNIQUE, pw_hash TEXT, admin BOOLEAN DEFAULT False);

CREATE TABLE posts(id SERIAL PRIMARY KEY, userid INTEGER NOT NULL, content TEXT NOT NULL, date timestamp NOT NULL DEFAULT now());

INSERT INTO users (name, email, pw_hash, admin) VALUES ('bigbob9', 'bobbybobson@outlook.com', 'skrrrt', False);
INSERT INTO users (name, email, pw_hash, admin) VALUES ('snow13', 'okeeffe.nikita@gmail.com', '$2b$12$H3bLAcyhibTK6O.3DKbrx.zI4ImQ9TRJwAhVFJnMf1ZlhTsOBDJgm', True);

CREATE TABLE messages (id SERIAL PRIMARY KEY, username TEXT, message TEXT);
