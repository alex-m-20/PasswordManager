import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

from models import db, User

load_dotenv()  # reads .env into the environment (SECRET_KEY, ENCRYPTION_KEY)

login_manager = LoginManager()
login_manager.login_view = "login"  # sends anyone not logged in to the login page

csrf = CSRFProtect()   # checks every form submission for a valid CSRF token


@login_manager.user_loader
def load_user(user_id):
    """
    Since user_id arrives as text, the int() converts it to a number
    then returns the matching row from the users table.
    """
    return User.query.get(int(user_id))




def create_app() -> Flask:
    app = Flask(__name__)

    # if SECRET_KEY isn't set in the .env file, fall back to this placeholder instead
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "SECRET_KEY is missing")
    os.makedirs(app.instance_path, exist_ok=True)

    # builds the full path to the SQLite database file, e.g. .../instance/password_manager.db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.instance_path, "password_manager.db"
    )

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    return app



# Builds the app then starts a local server when file is started directly.
if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True)