from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import EbayItem

class ItemForm(FlaskForm):
    item = StringField('Enter Ebay Item:', validators=[DataRequired()])
    submit = SubmitField('Create Graph')
    