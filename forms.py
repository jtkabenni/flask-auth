from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email
import email_validator


class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(),Email()])
    first_name = StringField("First name",validators=[InputRequired()])
    last_name= StringField("Last name",validators=[InputRequired()])


class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class AddFeedback(FlaskForm):
    title = StringField("Title", validators = [InputRequired()])
    content = StringField("Content", validators = [InputRequired()])



