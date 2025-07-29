-- Migration to add role column to allow_list table
ALTER TABLE allow_list ADD COLUMN role VARCHAR(50) NOT NULL DEFAULT 'Admin';