"""
Creates the database schema (the users and credentials tables), so the
app has somewhere to store data before registering the first account.

"""
from app import create_app
from models import db


def create_schema():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Schema created (or already present).")


if __name__ == "__main__":
    create_schema()