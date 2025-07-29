-- Migration to add threats table
CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address VARCHAR(45) NOT NULL,
    timestamp DATETIME NOT NULL,
    threat_type VARCHAR(50) NOT NULL,
    description TEXT,
    analyst_email VARCHAR(120) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);