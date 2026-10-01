"""
Routes decides what happens when someone visits a page on the site like
registering an account, logging
in and out and seeing the dashboard.
"""


from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models import db, User
from forms import RegistrationForm, LoginForm


def register_routes(app):
    # Everything below is grouped together here so it can all be handed
    # over to the actual app at once, from app.py.

    # The home page, just shows a simple welcome page to anyone who visits.
    @app.route("/")
    def index():
        return render_template("index.html")


    # Handles creating a new account. Shows the registration form and if
    # someone submits it correctly, creates their account and sends them
    # to the login page.
    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created - you can now log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)


    # Handles logging in. Shows the login form and if the username and
    # password match an existing account, logs them in and sends them to
    # the dashboard.
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
            flash("Incorrect username or password.", "error")
        return render_template("login.html", form=form)



    # Logs the current person out and sends them back to the login page.
    # Only works if someone is actually logged in.
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))



    # The main page someone sees once they're logged in.
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")