from sqlalchemy import ForeignKey
from app import db


class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    refresh_token = db.Column(db.String(50), unique=True)
    user_agent_hash = db.Column(db.String(80))
