"""
Routes decides what happens when someone visits a page on the site like
registering an account, logging
in and out and seeing the dashboard.
"""


from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from models import db, User, Credential
from forms import RegistrationForm, LoginForm, CredentialForm
from encryption import encrypt_password, decrypt_password


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

            # Check whether someone has already registered with this
            # username before creating the new account. Prevents crashes.
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("Username is already in use. Kindly pick another one...", "error")
                return render_template("register.html", form=form)

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




    # The main page someone sees once they're logged in. Shows all the
    # credentials they've saved so far.
    @app.route("/dashboard")
    @login_required
    def dashboard():
        credentials = Credential.query.filter_by(user_id=current_user.id).all()
        return render_template("dashboard.html", credentials=credentials)



    # Shows the "add a new credential" form when someone visits this
    # page normally. If they fill it in and submit, this takes the
    # password they typed, encrypts it and saves the new entry to the
    # database as belonging to whichever user is currently logged in.
    @app.route("/add_credential", methods=["GET", "POST"])
    @login_required
    def add_credential():
        form = CredentialForm()
        if form.validate_on_submit():
            encrypted = encrypt_password(form.site_password.data)
            new_credential = Credential(
                user_id=current_user.id,
                site_name=form.site_name.data,
                site_username=form.site_username.data,
                encrypted_password=encrypted,
            )
            db.session.add(new_credential)
            db.session.commit()
            flash("Credential saved.", "success")
            return redirect(url_for("dashboard"))
        return render_template("add_credential.html", form=form)



    # Shows one saved credential with its password actually decrypted, so the person can see what they saved. it 
    # only works for credentials that belong to whoever is currently logged in.
    @app.route("/reveal_credential/<int:credential_id>")
    @login_required
    def reveal_credential(credential_id):
        credential = Credential.query.get_or_404(credential_id)

        if credential.user_id != current_user.id:
            flash("You don't have permission to view that credential.", "error")
            return redirect(url_for("dashboard"))

        password = decrypt_password(credential.encrypted_password)
        return render_template("reveal_credential.html", credential=credential, password=password)



    # Deletes the saved credentials of the user who is logged in. Only responds to a form submission (a POST request)
    # to prevent deleting by accident. 
    @app.route("/delete_credential/<int:credential_id>", methods=["POST"])
    @login_required
    def delete_credential(credential_id):
        credential = Credential.query.get_or_404(credential_id)

        if credential.user_id != current_user.id:
            flash("You don't have permission to delete that credential.", "error")
            return redirect(url_for("dashboard"))

        db.session.delete(credential)
        db.session.commit()
        flash("Credential deleted.", "success")
        return redirect(url_for("dashboard"))



    # Shows a form containing the saved credentials, giving the
    # user a chance to make amends and update. 
    @app.route("/edit_credential/<int:credential_id>", methods=["GET", "POST"])
    @login_required
    def edit_credential(credential_id):
        credential = Credential.query.get_or_404(credential_id)

        if credential.user_id != current_user.id:
            flash("You don't have permission to edit that credential.", "error")
            return redirect(url_for("dashboard"))

        form = CredentialForm()

        if form.validate_on_submit():
            credential.site_name = form.site_name.data
            credential.site_username = form.site_username.data
            credential.encrypted_password = encrypt_password(form.site_password.data)
            db.session.commit()
            flash("Credential updated.", "success")
            return redirect(url_for("dashboard"))

        # Lists the credentials saved, instead of a blank form. Runs only when the user is just
        # visiting the page. 
        if request.method == "GET":
            form.site_name.data = credential.site_name
            form.site_username.data = credential.site_username
            form.site_password.data = decrypt_password(credential.encrypted_password)

        return render_template("edit_credential.html", form=form, credential=credential)