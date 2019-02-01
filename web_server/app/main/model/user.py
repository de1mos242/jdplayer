import enum
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from app.main import db, flask_bcrypt


class UserSource(enum.Enum):
    security = 'security'
    google = 'google'


class User(UserMixin, db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(50), unique=True)
    source = db.Column(db.Enum(UserSource), nullable=False, server_default=UserSource.security.value)

    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def load_by_id(cls, id):
        return User.query.get(int(id))


class SecurityUser(db.Model):
    """ storing login/password pairs to provide direct login mechanism"""
    __tablename__ = "security_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship(User.__name__)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Security User {self.username}>"


class GoogleUser(db.Model):
    """ storing credentials for goolge user """
    __tablename__ = "google_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_id = db.Column(db.Text, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship(User.__name__)

    def __repr__(self):
        return f"<Google user {self.username}>"
