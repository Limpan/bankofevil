from wtforms import SubmitField, TextField, PasswordField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    email = TextField('E-mail', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Register')
