from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    userID = StringField('userID', validators=[DataRequired(), Length(max=50)])
    idPhoto = FileField('Profile Picture', validators=[DataRequired()])

class IssueForm(FlaskForm):
    name = StringField('Issue Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('bug', 'Bug'), ('feature', 'Feature Request')], validators=[DataRequired()])
