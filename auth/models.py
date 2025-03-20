from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from apps.app import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    userIndex = db.Column(db.Integer, index=True)
    userId = db.Column(db.String(255), primary_key=True)
    userPassword = db.Column(db.String(255), nullable=False)
    userName = db.Column(db.String(255), index=True)
    userPhoneNumber = db.Column(db.String(255))
    userEmail = db.Column(db.String(255), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def get_id(self):
        return str(self.userId) 

    @property
    def password(self):
        raise AttributeError("읽어 들일 수 없음")

    @password.setter
    def password(self, password):
        self.userPassword = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.userPassword, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)