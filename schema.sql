CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role INTEGER
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    date TEXT,
    user_id INTEGER REFERENCES users,
    title TEXT,
    location TEXT,
    event_date TEXT,
    event_time TEXT,
    max_players INTEGER
);

CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    message_id INTEGER REFERENCES messages,
    user_id INTEGER REFERENCES users,
    UNIQUE (user_id, message_id)
);

CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);
