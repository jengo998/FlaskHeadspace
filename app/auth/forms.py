from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User

class UsernameForm(FlaskForm):
    new_username = StringField('New Username', validators=[DataRequired()])
    submit = SubmitField('Change username')

    def validate_new_username(self, new_username):
        user = User.query.filter_by(username=new_username.data).first()
        if user is not None:
            raise ValidationError("Username is already in use.")

class PasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    old_password = PasswordField('Confirm Old Password', validators=[DataRequired()])
    submit = SubmitField('Change password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already in use.")
