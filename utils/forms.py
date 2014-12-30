"""
Contains definitions of forms for various parts of the app
"""

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(Form):
    Username = TextField(
        'Username', validators=[DataRequired()]
    )
    Firstname = TextField(
        'Firstname', validators=[DataRequired()]
    )
    Lastname = TextField(
        'Lastname'
    )
    Password = PasswordField(
        'Password', validators=[DataRequired()]
    )

class LoginForm(Form):
    Username = TextField('Username', [DataRequired()])
    Password = PasswordField('Password', [DataRequired()])
