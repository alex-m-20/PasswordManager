"""
Web forms for registering a new account, logging in and saving a
new credentials. Built with Flask-WTF and it protects these forms
against CSRF attacks automatically.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class CredentialForm(FlaskForm):
    site_name = StringField("Site Name", validators=[DataRequired()])
    site_username = StringField("Username", validators=[DataRequired()])
    site_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Save")