from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AllowList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    from_allowed_ending = db.Column(db.Boolean, nullable=True)
    role = db.Column(db.String(50), nullable=False, default='Admin')

class BlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class AllowedEmailEndings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_ending = db.Column(db.String(120), unique=True, nullable=False)

class Threat(db.Model):
    __tablename__ = 'threats'  # Explicitly set table name to match existing table
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv4/IPv6 max length
    timestamp = db.Column(db.DateTime, nullable=False)
    threat_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    analyst_email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    region = db.Column(db.String(100))