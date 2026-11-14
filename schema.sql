create table users (
    id integer primary key,
    username text unique,
    password_hash text
);

create table messages (
    id integer primary key,
    content text,
    date text,
    user_id integer,
    title text
);

create table visits (
    id integer primary key,
    visited_at text
);