-- Migration to add BlockList table
CREATE TABLE IF NOT EXISTS block_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL
);