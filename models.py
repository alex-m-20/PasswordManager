"""
Two tables; users and credentials. 
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

# Database from SQLA that will be used by the whole app.
db = SQLAlchemy()




class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Links the user to all the credentials they have saved. 
    credentials = db.relationship(
        "Credential",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"




class Credential(db.Model):
    __tablename__ = "credentials"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    site_name = db.Column(db.String(120), nullable=False)
    site_username = db.Column(db.String(120), nullable=False)
    encrypted_password = db.Column(db.LargeBinary, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_modified = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
)

    def __repr__(self):
        return f"<Credential id={self.id} site={self.site_name!r} user_id={self.user_id}>"