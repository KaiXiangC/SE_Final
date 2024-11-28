from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    userID = StringField('userID', validators=[DataRequired(), Length(max=50)])
    idPhoto = FileField('Profile Picture', validators=[DataRequired()])