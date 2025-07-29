-- Migration to add from_allowed_ending column to allow_list table
ALTER TABLE allow_list ADD COLUMN from_allowed_ending BOOLEAN;