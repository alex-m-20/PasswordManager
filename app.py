import os

from flask import Flask
from dotenv import load_dotenv

from models import db

load_dotenv()  # reads .env into the environment (SECRET_KEY, ENCRYPTION_KEY)

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

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True)