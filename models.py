import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

def gen_uuid():
    return str(uuid.uuid4())

class Scheme(db.Model):
    __tablename__ = 'schemes'
    id = db.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    code = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(128))
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    min_income = db.Column(db.Integer)
    max_income = db.Column(db.Integer)
    target_gender = db.Column(db.String(16))
    states_applicable = db.Column(JSON)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    official_url = db.Column(db.String(512))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    translations = db.relationship('SchemeTranslation', backref='scheme', cascade='all, delete-orphan')

class SchemeTranslation(db.Model):
    __tablename__ = 'scheme_translations'
    id = db.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    scheme_id = db.Column(UUID(as_uuid=False), db.ForeignKey('schemes.id'), nullable=False)
    lang = db.Column(db.String(8), nullable=False)
    title = db.Column(db.Text)
    short_desc = db.Column(db.Text)
    full_desc = db.Column(db.Text)
    instructions = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
