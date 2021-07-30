from datetime import datetime, date, timedelta
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_exercised = db.Column(db.Date, index=True, default=date.today)
    exercise_day = db.relationship('ExerciseDay', backref='author', lazy='dynamic')
    streak = db.relationship('Streak', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=retro&s={}'.format(digest, size)


class ExerciseDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daily_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    streak_id = db.Column(db.Integer, db.ForeignKey('streak.id'))

    def __repr__(self):
        return '<Exercise {}>'.format(self.daily_count)

class Streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_count = db.Column(db.Integer, index=True)
    streak_begin = db.Column(db.Date, index=True)
    streak_end = db.Column(db.Date, index=True)
    exercise_day = db.relationship('ExerciseDay', backref='streak', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref='streak', lazy='dynamic')

    def __repr__(self):
        return '<Streak {}>'.format(self.total_count)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
