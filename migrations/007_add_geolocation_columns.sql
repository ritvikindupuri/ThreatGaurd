-- Migration to add geolocation columns to threats table
ALTER TABLE threats ADD COLUMN country VARCHAR(100);
ALTER TABLE threats ADD COLUMN city VARCHAR(100);
ALTER TABLE threats ADD COLUMN latitude REAL;
ALTER TABLE threats ADD COLUMN longitude REAL;
ALTER TABLE threats ADD COLUMN region VARCHAR(100);