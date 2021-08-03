from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User

class JournalForm(FlaskForm):
    post_date = StringField('Write date:', validators=[DataRequired()])
    post = TextAreaField('Write post:', validators=[DataRequired(), Length(min=0, max=4000)])
    submit = SubmitField('Post')
    delete = SubmitField('Delete Last Post')