from datetime import datetime, date, timedelta
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    daily_count = db.Column(db.Integer, default=0)
    last_exercised = db.Column(db.Date, index=True, default=date.today)
    streak = db.relationship('Streak', back_populates='user', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=retro&s={}'.format(digest, size)


class Streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_count = db.Column(db.Integer, index=True)
    streak_begin = db.Column(db.Date, index=True)
    streak_end = db.Column(db.Date, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates='streak', uselist=False)
    old_user = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Streak {} {}>'.format(self.streak_begin, self.old_user)


class PostDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(2000))
    post_date = db.Column(db.String(32), index=True)

    def __repr__(self):
        return 'Post {}'.format(self.post_date)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
