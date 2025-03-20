from datetime import datetime

from apps.app import db
from apps.auth.models import User

class Board(db.Model):
    __tablename__ = "board"
    boardId = db.Column(db.Integer, primary_key=True)
    boardTitle = db.Column(db.String(255))
    boardContent = db.Column(db.String(255))
    boardRating = db.Column(db.Integer)
    boardCreate = db.Column(db.DateTime, default=datetime.now)
    boardUpdate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)        
    userId = db.Column(db.String(255), db.ForeignKey("users.userId"))
    boardImage = db.Column(db.String(255))
    user = db.relationship("User", backref="posts")