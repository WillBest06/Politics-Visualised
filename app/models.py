from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    favourite_mps = db.relationship('FavouriteMP', back_populates='user', cascade="all, delete-orphan")
    saved_petitions = db.relationship('SavedPetition', back_populates='user', cascade="all, delete-orphan")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class SavedPetition(db.Model):
    __tablename__ = 'saved_petition'
    id               = db.Column(db.Integer, primary_key=True) 
    petition_id      = db.Column(db.Integer, nullable=False)
    creation_date    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title            = db.Column(db.String(100), nullable=False)
    details          = db.Column(db.Text, nullable=False)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='saved_petitions')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class FavouriteMP(db.Model):
    __tablename__    = 'favourite_mp'
    id               = db.Column(db.Integer, primary_key=True)
    creation_date    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    member_id        = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='favourite_mps')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self